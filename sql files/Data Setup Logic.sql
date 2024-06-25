delete from style_master where style is null;

alter table style_master modify brand_lookup varchar(65);

update style_master set class = trim(class);
update style_master set INVENTORY_SIZE = trim(INVENTORY_SIZE);
update style_master set color_code = trim(color_code);
update case_breakdown set class_cd = trim(class_cd);
update case_breakdown set INV_SZ = trim(INV_SZ);
update color_codes set PROD_CLR = trim(PROD_CLR);
update po_data_by_size set class_cd = trim(class_cd);
update po_data_by_size set PROD_CLR = trim(PROD_CLR);
update case_breakdown set class_cd = trim(class_cd);
update color_codes set PROD_CLR = trim(PROD_CLR);
update po_data_by_size set prod_cd = trim(prod_cd);

update style_master set IMAGE_FILE = replace(IMAGE_FILE, "D:\\JOSSHO\\omsphotos", 'V:')   where IMAGE_FILE like 'D:%';
update po_data_by_size set IMAGE_NM = replace(IMAGE_NM, "D:\\JOSSHO\\omsphotos", 'V:')   where IMAGE_NM like 'D:%';
update inventory_data set IMAGE = replace(IMAGE, "D:\\JOSSHO\\omsphotos", 'V:')   where IMAGE like 'D:%';




drop table if exists inventory_logic;
create table if not exists inventory_logic(primary key(STYLE, COLOR))
SELECT "Inventory" as DATA_TYPE, 
A.style, IFNULL(A.color,"") AS COLOR,
c.Size_Run,
c.Size_Breakdown,
c.Pack_Breakdown,
ifnull(C.Pack_Qty,A.PAIRS) as Pairs,
CONCAT(c.Size_Run, " Total Case Pairs =",CASE WHEN ifnull(C.Pack_Qty,A.PAIRS) != 0 THEN ifnull(C.Pack_Qty,A.PAIRS) ELSE SUM(A.PPK_PACK) END ) as CASE_DETAILS,  
A.IMAGE_FILE as IMAGE, 
A.Note,
A.Brand_lookup as Brand,
A.DESCRIPTION,
"AT ONCE" AS DATE, 
1 AS DATE_ORDER,
sum(IFNULL(B.INVENTORY_QTY,0)) as QUANTITY,
SUM(IFNULL(B.SALES_ORDER_QTY,0)) AS SALES_QTY,
SUM(IFNULL(B.AVAILABLE_QTY,0)) AS AVAILABLE_QTY,
CASE WHEN SUM(IFNULL(B.AVAILABLE_QTY,0)) >0 THEN SUM(IFNULL(B.AVAILABLE_QTY,0)) ELSE 0 END AS ADJUSTED_AVAILABLE_QTY,
0 as PO_QTY,
B.SIZE_PO_QTY,
SUM(IFNULL(B.ALLOCATED_QTY,0)) AS ALLOCATED_QTY,
SUM(IFNULL(B.REAL_ALLOCATED_QTY,0)) AS REAL_ALLOCATED_QTY,
ifnull(B.RETAIL_PRS,A.RETAIL_PRS) as RETAIL_PRS,  ifnull(B.WHOLE_PRS,A.WHOLE_PRS) as WHOLE_PRS, A.PRICE_BASE, A.FRT_CUS, A.PROD_DUTY, A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS as AVG_COST
FROM style_master A
left join inventory_data B on A.style = b.prod_cd and a.color_code = b.PROD_CLR and a.size = B.Size_Breakdown
left join case_breakdown c on A.class = c.class_cd AND A.INVENTORY_SIZE = c.INV_SZ
left join color_codes d on A.color_code = d.PROD_CLR
where A.WHS_NUM = "01"
group by  A.style, A.color;



DROP TABLE IF EXISTS po_logic;
CREATE TABLE IF NOT EXISTS po_logic(primary key(style, color, DATE))
select "PO" as DATA_TYPE, A.prod_cd AS STYLE, C.CLR_DESC AS COLOR,
B.Size_Run, B.Size_Breakdown,
B.Pack_Breakdown,
A.PAIRS,
CONCAT(b.Size_Run, " Total Case Pairs =",A.PAIRS) as CASE_DETAILS,  
A.IMAGE_NM,
D.Note,
D.Brand,
D.DESCRIPTION,
EST_DT + INTERVAL 14 DAY AS DATE, 
1 + ROW_NUMBER() OVER (PARTITION BY A.prod_cd, C.CLR_DESC ORDER BY EST_DT) AS DATE_ORDER,
D.QUANTITY,
D.SALES_QTY,
D.AVAILABLE_QTY,
D.ADJUSTED_AVAILABLE_QTY,
SUM(A.PO_QTY) AS PO_QTY,
D.ALLOCATED_QTY AS ALLOCATED_QTY,
D.REAL_ALLOCATED_QTY AS REAL_ALLOCATED_QTY,
D.RETAIL_PRS as RETAIL_PRS, 
A.WHOLE_PRS, 
A.PRICE_BASE, 
D.FRT_CUS as FRT_CUS, 
D.PROD_DUTY as PROD_DUTY,
--    A.PRICE_BASE + (A.PRICE_BASE* (D.PROD_DUTY/100)) + D.FRT_CUS AS AVG_COST
A.PRICE_BASE AS AVG_COST
from po_data_by_size A
left join case_breakdown B on A.class_cd = B.class_cd
left join color_codes C on A.PROD_CLR = C.PROD_CLR
left join inventory_logic D on A.prod_cd = D.style and C.CLR_DESC = D.color
-- where PROD_CD like"AV89401M%"
group by  A.PROD_CD, C.CLR_DESC, A.EST_DT;


drop table if exists available_inventory_setup;
create table if not exists available_inventory_setup(primary key(DATA_TYPE, style, color, DATE))
	select *, case when DATA_TYPE = "Inventory" then ADJUSTED_AVAILABLE_QTY 
					WHEN DATA_TYPE  = "PO" then updated_po_qty end as final_qty from
	(select *, 0 as updated_po_qty from inventory_logic 
	-- where ADJUSTED_AVAILABLE_QTY > 0
	union
	select DATA_TYPE, STYLE, COLOR, Size_Run, Size_Breakdown, Pack_Breakdown, Pairs, CASE_DETAILS, IMAGE_NM, 
    Note, Brand, DESCRIPTION, DATE, DATE_ORDER, QUANTITY, SALES_QTY, 
	AVAILABLE_QTY, ADJUSTED_AVAILABLE_QTY, PO_QTY,PO_QTY as SIZE_PO_QTY, ALLOCATED_QTY, REAL_ALLOCATED_QTY, RETAIL_PRS, WHOLE_PRS, PRICE_BASE, FRT_CUS, PROD_DUTY,  
	PRICE_BASE + (PRICE_BASE* (PROD_DUTY/100)) + FRT_CUS AS AVG_COST, updated_po_qty
	from
	(
	select *, 
	case when AVAILABLE_QTY < 0 then 
			case when cumulative_pos > abs(AVAILABLE_QTY) then least(cumulative_pos-abs(AVAILABLE_QTY), PO_QTY)  
			 when cumulative_pos <= abs(AVAILABLE_QTY) then 0
		   end 
		  when AVAILABLE_QTY >=0 then 
			case when AVAILABLE_QTY >= cumulative_pos then PO_QTY
				when AVAILABLE_QTY < cumulative_pos then 
					case when SALES_QTY >QUANTITY then  least(cumulative_pos-abs(AVAILABLE_QTY), PO_QTY)
								when SALES_QTY <=QUANTITY then PO_QTY
					end
			end 
	end  as updated_po_qty from
	(select *, sum(PO_QTY) over (partition by style, color order by DATE asc) as cumulative_pos from po_logic) A
) B
order by STYLE , color, DATE_ORDER) A;
    

   Alter table available_inventory_setup add column total_qty int;
   Alter table available_inventory_setup modify Pack_Breakdown varchar(255);
   UPDATE available_inventory_setup SET Pack_Breakdown = REPLACE(REPLACE(REPLACE(Pack_Breakdown," ","_"),"__","_"),"_","   ");

   update available_inventory_setup A inner join
    (select STYLE, COLOR, sum(final_qty) as total_qty from available_inventory_setup group by STYLE, COLOR) B using(style, color)
    set a.total_qty = b.total_qty ;

   drop table if exists no_size_run_data_setup;
   create table if not exists no_size_run_data_setup(primary key(STYLE, color,DATE))
        Select * from
        (select 
        ROW_NUMBER() OVER (PARTITION BY STYLE ORDER BY STYLE, COLOR, DATE_ORDER) AS ID,
        DATE_ORDER,STYLE, COLOR,
        STYLE AS CORE_STYLE, COLOR AS CORE_COLOR, DATE as CORE_DATE,
        Size_Run, IMAGE, 
		Note, Brand, DESCRIPTION,
        DATE,  final_qty as Quantity,
        final_qty AS Lookup_Quantity,
        pairs,
        case 
         when final_qty = 0 then 0
        when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
        else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end
        as cases,
        case 
         when final_qty = 0 then 0
        when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
        else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end
        as Lookup_cases,
        WHOLE_PRS as price, PRICE_BASE as cost, 
        max_cost  as landed_cost 
        from available_inventory_setup A
        left join (select PROD_CD as style, max( A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS) as max_cost from inventory_data A group by PROD_CD) B using(style)
        ORDER BY STYLE,COLOR, DATE_ORDER) A
        where Quantity >0;
        

   drop table if exists no_size_run_data_setup_all;
   create table if not exists no_size_run_data_setup_all(primary key(STYLE, color,DATE))
        Select * from
        (select 
        ROW_NUMBER() OVER (PARTITION BY STYLE ORDER BY STYLE, COLOR, DATE_ORDER) AS ID,
        DATE_ORDER,STYLE, COLOR,
        STYLE AS CORE_STYLE, COLOR AS CORE_COLOR, DATE as CORE_DATE,
        Size_Run, IMAGE, 
        Note, Brand, DESCRIPTION,
        DATE,  final_qty as Quantity,
        final_qty AS Lookup_Quantity,
        pairs,
        case 
        when final_qty = 0 then 0
        when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
        else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end
        as cases,
        case 
        when final_qty = 0 then 0
        when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
        else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end
        as Lookup_cases,
        WHOLE_PRS as price, PRICE_BASE as cost, 
        max_cost  as landed_cost 
        from available_inventory_setup A
        left join (select PROD_CD as style, max( A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS) as max_cost from inventory_data A group by PROD_CD) B using(style)
        ORDER BY STYLE,COLOR, DATE_ORDER) A;

   drop table if exists ID_SETUP;
   CREATE TABLE if not exists ID_SETUP(
    ID INT PRIMARY KEY
    );

   INSERT INTO ID_SETUP VALUES
    (1),(2),(3);

   drop table if exists size_run_data_setup;
    create table if not exists size_run_data_setup(primary key(ID, Core_Style, core_color, core_date))
select ID, STYLE as Core_Style,COLOR as core_color,DATE as core_date, DATE_ORDER, case when ID = 1 then STYLE else "" end as STYLE,
    case when ID = 1 then COLOR else "" end as COLOR,
    case when ID = 1 then CASE_DETAILS 
    	 when ID = 2 then Size_Breakdown
    	 when ID = 3 then Pack_Breakdown
     end as Size_Run,
    case when ID = 1 then IMAGE else "" end as IMAGE,
	case when ID = 1 then Note else "" end as Note,
	case when ID = 1 then Brand else "" end as Brand,
	case when ID = 1 then DESCRIPTION else "" end as DESCRIPTION,
    case when ID = 1 then DATE else "" end as DATE,
    case when ID = 1 then final_qty else "" end as Quantity,
    final_qty AS Lookup_Quantity,
    case when ID = 1 then 
    	case 
    	when final_qty = 0 then 0
    	when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
    	else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end
        end as Cases,
    case 
        when final_qty = 0 then 0
        when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
    	else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end as Lookup_cases,
    case when ID = 1 then WHOLE_PRS else "" end as price,
    case when ID = 1 then PRICE_BASE else "" end as cost,
    case when ID = 1 then max_cost else "" end as landed_cost
    from 
    (select * 
    from ID_SETUP
    cross join 
    (
    select A.*, B.max_cost 
    from available_inventory_setup A
	left join (select PROD_CD as style, max( A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS) as max_cost from inventory_data A group by PROD_CD) B using(style)
    where final_qty !=0
    ) A) A;

   drop table if exists size_run_data_setup_all;
   create table if not exists size_run_data_setup_all(primary key(ID, Core_Style, core_color, core_date))
select ID, STYLE as Core_Style,COLOR as core_color,DATE as core_date, DATE_ORDER, case when ID = 1 then STYLE else "" end as STYLE,
    case when ID = 1 then COLOR else "" end as COLOR,
    case when ID = 1 then CASE_DETAILS 
    	 when ID = 2 then Size_Breakdown
    	 when ID = 3 then Pack_Breakdown
     end as Size_Run,
    case when ID = 1 then IMAGE else "" end as IMAGE,
    case when ID = 1 then Note else "" end as Note,
	case when ID = 1 then Brand else "" end as Brand,
	case when ID = 1 then DESCRIPTION else "" end as DESCRIPTION,
    case when ID = 1 then DATE else "" end as DATE,
    case when ID = 1 then final_qty else "" end as Quantity,
    final_qty AS Lookup_Quantity,
    case when ID = 1 then 
    	case 
    	when final_qty = 0 then 0
    	when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
    	else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end
        end as Cases,
    case 
        when final_qty = 0 then 0
          when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
    	else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end as Lookup_cases,
    case when ID = 1 then WHOLE_PRS else "" end as price,
    case when ID = 1 then PRICE_BASE else "" end as cost,
    case when ID = 1 then max_cost else "" end as landed_cost
    from 
    (select * 
    from ID_SETUP
    cross join 
    (
    select A.*, B.max_cost 
    from available_inventory_setup A
	left join (select PROD_CD as style, max( A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS) as max_cost from inventory_data A group by PROD_CD) B using(style)
    ) A) A;
    
    

   drop table if exists upc_data;
   create table if not exists upc_data
select id,
    0 AS DATE_ORDER,
    ACTIVE as Status,
    style as Core_Style, color as Core_Color,
    style, color, ifnull(size,"") as size, 
    case when id = 1 then CASE_DETAILS 
    	when id = 2 then Size_Breakdown 
    	when id = 3 then Pack_Breakdown
        end as size_run,
        IMAGE,
        Note, Brand, Description,
        UPC, WHOLE_PRS as price, PRICE_BASE as cost, max_cost as landed_cost,
		INVENTORY_QTY,
		SIZE_PO_QTY,
		SALES_ORDER_QTY,
		ATS,
		AVAILABLE_QTY,
		`IN STOCK`,
        INCOMING
     from
    (
    SELECT 
    row_number() over (partition by A.STYLE, ifnull(C.CLR_DESC,"") order by  A.STYLE, ifnull(C.CLR_DESC,""), A.NUMBER, A.Size) as id,
    A.ACTIVE,
    A.STYLE as STYLE, ifnull(C.CLR_DESC,"") AS COLOR,
    b.Size_Run,
    A.Size as Size,
    B.Size_Breakdown,
    B.Pack_Breakdown,
    A.PAIRS,
    A.Note, A.Brand, A.Description,
    CONCAT(b.Size_Run, " Total Case Pairs =",A.PAIRS) as CASE_DETAILS,
    IMAGE_FILE AS IMAGE,
	EXPANDED_UPC as UPC,
    A.WHOLE_PRS,
    A.PRICE_BASE, 
    A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS as AVG_COST,
    D.max_cost ,
    E.INVENTORY_QTY,
    E.SIZE_PO_QTY,
	E.SALES_ORDER_QTY,
	E.AVAILABLE_TO_SELL_QTY AS ATS,
	E.AVAILABLE_QTY,
    case when E.SALES_ORDER_QTY = 0 then  	E.AVAILABLE_QTY
		when (E.SALES_ORDER_QTY - E.INVENTORY_QTY) <=0 then E.INVENTORY_QTY - E.SALES_ORDER_QTY 
		when (E.SALES_ORDER_QTY - E.INVENTORY_QTY) >0 then 0
	end as `IN STOCK`,
        
     case when E.SALES_ORDER_QTY = 0 then E.SIZE_PO_QTY
		  when (E.SALES_ORDER_QTY - E.INVENTORY_QTY) <=0 then E.SIZE_PO_QTY
			when (E.SALES_ORDER_QTY - E.INVENTORY_QTY) - E.SIZE_PO_QTY >=0 then 0 
            
			when (E.SALES_ORDER_QTY - E.INVENTORY_QTY) - E.SIZE_PO_QTY <0 THEN E.SIZE_PO_QTY + ((E.INVENTORY_QTY - E.SALES_ORDER_QTY))
		end AS INCOMING
        from 
    style_master A
    left join case_breakdown B on A.CLASS = B.class_cd  and A.INVENTORY_SIZE = b.inv_sz 
    left join color_codes C on  A.COLOR_CODe = C.PROD_CLR
	left join (select PROD_CD as style, Prod_clr as color,  max( A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS) as max_cost from inventory_data A group by PROD_CD, Prod_clr) D on A.STYLE = D.style and A.color_code = D.color
    left join inventory_data E on A.style = E.prod_cd and A.color = e.prod_clr and a.size = e.size_breakdown
    where A.WHS_NUM = "01"
     ) A;
     

drop table if exists inventory_logic_by_size;
create table if not exists inventory_logic_by_size(primary key(STYLE, COLOR, SIZE))
SELECT "Inventory" as DATA_TYPE, 
A.style, IFNULL(A.color,"") AS COLOR,a.NUMBER AS Size_Order,
ifnull(A.Size,"") as Size ,
A.PPK_PACK, 
c.Size_Run,
c.Size_Breakdown,
c.Pack_Breakdown,
A.PAIRS,
CONCAT(c.Size_Run, " Total Case Pairs =",A.PAIRS) as CASE_DETAILS,  
A.IMAGE_FILE as IMAGE, 
A.Note, A.Brand, A.Description,
"AT ONCE" AS DATE, 
1 AS DATE_ORDER,
sum(IFNULL(B.INVENTORY_QTY,0)) as QUANTITY,
SUM(IFNULL(B.SALES_ORDER_QTY,0)) AS SALES_QTY,
SUM(IFNULL(B.AVAILABLE_QTY,0)) AS AVAILABLE_QTY,
CASE WHEN SUM(IFNULL(B.AVAILABLE_QTY,0)) >0 THEN SUM(IFNULL(B.AVAILABLE_QTY,0)) ELSE 0 END AS ADJUSTED_AVAILABLE_QTY,
0 as PO_QTY,
B.SIZE_PO_QTY,
SUM(IFNULL(B.ALLOCATED_QTY,0)) AS ALLOCATED_QTY,
SUM(IFNULL(B.REAL_ALLOCATED_QTY,0)) AS REAL_ALLOCATED_QTY,
ifnull(B.RETAIL_PRS,A.RETAIL_PRS) as RETAIL_PRS,  ifnull(B.WHOLE_PRS,A.WHOLE_PRS) as WHOLE_PRS, A.PRICE_BASE, A.FRT_CUS, A.PROD_DUTY, A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS as AVG_COST
FROM style_master A
left join inventory_data B on A.style = b.prod_cd and a.color_code = b.PROD_CLR and a.size = B.Size_Breakdown
left join case_breakdown c on A.class = c.class_cd AND A.INVENTORY_SIZE = c.INV_SZ
left join color_codes d on A.color_code = d.PROD_CLR
-- and  A.SZ_RUN = B.inv_sz
-- where PROD_CD like"BH88935H%"
 where A.WHS_NUM = "01"
group by  A.style, A.color, A.Size;



   DROP TABLE IF EXISTS po_logic_by_size;
   CREATE TABLE IF NOT EXISTS po_logic_by_size(primary key(style, color, size, DATE))
        select "PO" as DATA_TYPE, A.prod_cd AS STYLE, C.CLR_DESC AS COLOR,
        a.NUMBER AS Size_Order,
        A.Size_Breakdown as Size,
        B.Size_Run, 
        B.Size_Breakdown,
        B.Pack_Breakdown,
        A.PAIRS,
        CONCAT(b.Size_Run, " Total Case Pairs =",A.PAIRS) as CASE_DETAILS,  
        A.IMAGE_NM,
        D.Note, D.Brand, D.Description,
        EST_DT + INTERVAL 14 DAY AS DATE, 
        1 + dense_rank() OVER (PARTITION BY A.prod_cd, C.CLR_DESC ORDER BY EST_DT) AS DATE_ORDER,

        D.QUANTITY,
        D.SALES_QTY,
        D.AVAILABLE_QTY,
        D.ADJUSTED_AVAILABLE_QTY,
        SUM(A.PO_QTY) AS PO_QTY,
        D.ALLOCATED_QTY AS ALLOCATED_QTY,
        D.REAL_ALLOCATED_QTY AS REAL_ALLOCATED_QTY,
        D.RETAIL_PRS as RETAIL_PRS, 
        A.WHOLE_PRS, 
        A.PRICE_BASE, 
        D.FRT_CUS as FRT_CUS, 
        D.PROD_DUTY as PROD_DUTY,
        -- A.PRICE_BASE + (A.PRICE_BASE* (D.PROD_DUTY/100)) + D.FRT_CUS AS AVG_COST
        A.PRICE_BASE AS AVG_COST
        from po_data_by_size A
        left join case_breakdown B on A.class_cd = B.class_cd
        left join color_codes C on A.PROD_CLR = C.PROD_CLR
        left join inventory_logic D on A.prod_cd = D.style and C.CLR_DESC = D.color
        group by  A.PROD_CD, C.CLR_DESC,A.Size_Breakdown, A.EST_DT;
        

   DROP TABLE IF EXISTS po_logic_by_size_run;
   CREATE TABLE IF NOT EXISTS po_logic_by_size_run(primary key(style, color, size, Stock_Makeup, DATE))
        select "PO" as DATA_TYPE, 
        Case when B.Size_Run is not null then "Size Run" else "No Size Run" end as Stock_Makeup,
        A.prod_cd AS STYLE, C.CLR_DESC AS COLOR,
        a.NUMBER AS Size_Order,
        A.Size_Breakdown as Size,
        A.Size_Pack_Qty as PPK_QTY,
        B.Size_Run, 
        B.Size_Breakdown,
        B.Pack_Breakdown,
        A.PAIRS,
        CONCAT(b.Size_Run, " Total Case Pairs =",A.PAIRS) as CASE_DETAILS,  
        A.IMAGE_NM,
        D.Note, D.Brand, D.Description,
        EST_DT + INTERVAL 14 DAY AS DATE, 
        1 + dense_rank() OVER (PARTITION BY A.prod_cd, C.CLR_DESC ORDER BY EST_DT) AS DATE_ORDER,
        D.QUANTITY,
        D.SALES_QTY,
        D.AVAILABLE_QTY,
        D.ADJUSTED_AVAILABLE_QTY,
        SUM(A.PO_QTY) AS PO_QTY,
        D.ALLOCATED_QTY AS ALLOCATED_QTY,
        D.REAL_ALLOCATED_QTY AS REAL_ALLOCATED_QTY,
        D.RETAIL_PRS as RETAIL_PRS, 
        A.WHOLE_PRS, 
        A.PRICE_BASE, 
        D.FRT_CUS as FRT_CUS, 
        D.PROD_DUTY as PROD_DUTY,
        -- A.PRICE_BASE + (A.PRICE_BASE* (D.PROD_DUTY/100)) + D.FRT_CUS AS AVG_COST
        A.PRICE_BASE AS AVG_COST
        from po_data_by_size A
        left join case_breakdown B on A.class_cd = B.class_cd and A.run_cd = B.inv_sz
        left join color_codes C on A.PROD_CLR = C.PROD_CLR
        left join inventory_logic D on A.prod_cd = D.style and C.CLR_DESC = D.color
        group by  A.PROD_CD, C.CLR_DESC,A.Size_Breakdown, A.EST_DT,  Case when B.Size_Run is not null then "Size Run" else "No Size Run" end;


   drop table if exists available_inventory_setup_by_size;
   create table if not exists available_inventory_setup_by_size(primary key(DATA_TYPE, style, color,size, DATE))
             select *, case when DATA_TYPE = "Inventory" then ADJUSTED_AVAILABLE_QTY 
                            WHEN DATA_TYPE  = "PO" then updated_po_qty end as final_qty from
            (select *, 0 as updated_po_qty from inventory_logic_by_size 
            -- where ADJUSTED_AVAILABLE_QTY > 0
            union
            select DATA_TYPE, STYLE, COLOR, size_order, size, null, Size_Run, Size_Breakdown, Pack_Breakdown, Pairs, CASE_DETAILS, IMAGE_NM,
               Note, Brand, Description,
            
            DATE, DATE_ORDER, QUANTITY, SALES_QTY, 
            AVAILABLE_QTY, ADJUSTED_AVAILABLE_QTY, PO_QTY,PO_QTY as Size_PO_QTY, ALLOCATED_QTY, REAL_ALLOCATED_QTY, RETAIL_PRS, WHOLE_PRS, PRICE_BASE, FRT_CUS, PROD_DUTY,  
            PRICE_BASE + (PRICE_BASE* (PROD_DUTY/100)) + FRT_CUS AS AVG_COST, updated_po_qty
            from
            (
            select *, 
            case when AVAILABLE_QTY < 0 then 
                    case when cumulative_pos > abs(AVAILABLE_QTY) then least(cumulative_pos-abs(AVAILABLE_QTY), PO_QTY)  
                     when cumulative_pos <= abs(AVAILABLE_QTY) then 0
                   end 
                  when AVAILABLE_QTY >=0 then 
                    case when AVAILABLE_QTY >= cumulative_pos then PO_QTY
                        when AVAILABLE_QTY < cumulative_pos then 
                            case when SALES_QTY >QUANTITY then  least(cumulative_pos-abs(AVAILABLE_QTY), PO_QTY)
                                        when SALES_QTY <=QUANTITY then PO_QTY
                            end
                    end 
            end  as updated_po_qty from
            (select *, sum(PO_QTY) over (partition by style, color, size order by DATE asc) as cumulative_pos from po_logic_by_size) A
        ) B
        order by STYLE , color, DATE_ORDER, size) A;

   Alter table available_inventory_setup_by_size add column total_qty int;
   Alter table available_inventory_setup_by_size modify Pack_Breakdown varchar(255); 
   UPDATE available_inventory_setup_by_size SET Pack_Breakdown = REPLACE(REPLACE(REPLACE(Pack_Breakdown," ","_"),"__","_"),"_","   ");
   update available_inventory_setup_by_size A inner join
    (select STYLE, COLOR, size, sum(final_qty) as total_qty from available_inventory_setup_by_size group by STYLE, COLOR, size) B using(style, color, size)
    set a.total_qty = b.total_qty ;

   drop table if exists no_size_run_data_setup_by_size;
   create table if not exists no_size_run_data_setup_by_size(primary key(STYLE, color,size, DATE))
        Select * from
        (select 
        ROW_NUMBER() OVER (PARTITION BY STYLE ORDER BY STYLE, COLOR, DATE_ORDER) AS ID,
        DATE_ORDER,STYLE, COLOR,size_order, SIZE, 
        STYLE AS CORE_STYLE, COLOR AS CORE_COLOR, DATE AS CORE_DATE,
        Size_Run, IMAGE, 
		Note, Brand, Description,
        DATE,  final_qty as Quantity,
        final_qty AS Lookup_Quantity,
        pairs,
        case when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
        else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end
        as cases,
        case when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
        else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
        end
        as Lookup_cases,
        WHOLE_PRS as price, PRICE_BASE as cost, 
        max_cost  as landed_cost 
        from available_inventory_setup_by_size A
        left join (select PROD_CD as style, max( A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS) as max_cost from inventory_data A group by PROD_CD) B using(style)
        ORDER BY STYLE,COLOR, DATE_ORDER, size_order) A;

   drop table if exists size_run_data_setup_by_size;
   create table if not exists size_run_data_setup_by_size(primary key(ID, Core_Style, core_color,Size, core_date))
         select ID, STYLE as Core_Style,COLOR as core_color,Size_Order, Size, DATE as core_date, DATE_ORDER, case when ID = 1 then STYLE else "" end as STYLE,
            case when ID = 1 then COLOR else "" end as COLOR,
            case when ID = 1 AND Size_Order =1 then CASE_DETAILS 
                 when ID = 2 AND Size_Order =1 then Size_Breakdown
                 when ID = 3 AND Size_Order =1 then Pack_Breakdown
             end as Size_Run,
            case when ID = 1 then IMAGE else "" end as IMAGE,
			case when ID = 1 then Note else "" end as Note,
			case when ID = 1 then Brand else "" end as Brand,
            case when ID = 1 then Description else "" end as Description,
            case when ID = 1 then DATE else "" end as DATE,
            case when ID = 1 then final_qty else "" end as Quantity,
            final_qty AS Lookup_Quantity,
            case when ID = 1 then 
                case when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
                else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
                end
                end as Cases,
            case when final_qty/case when pairs = 0 then 1 else pairs  end <1 then 1 
                else floor(final_qty/case when pairs = 0 then 1 else pairs  end)
                end as Lookup_cases,
            case when ID = 1 then WHOLE_PRS else "" end as price,
            case when ID = 1 then PRICE_BASE else "" end as cost,
            case when ID = 1 then max_cost else "" end as landed_cost
            from 
            (select * 
            from ID_SETUP
            cross join 
            (
            select A.*, B.max_cost 
            from available_inventory_setup_by_size A
            left join (select PROD_CD as style, max( A.PRICE_BASE + (A.PRICE_BASE* (A.PROD_DUTY/100)) + A.FRT_CUS) as max_cost from inventory_data A group by PROD_CD
            ) B using(style)
            ) A) A;
            
-- -----------------------------------------------------------------------------
-- Inventory Report Setup ------------------------------------------------------
-- -----------------------------------------------------------------------------


drop table if exists inventory_detail_setup;
create table if not exists inventory_detail_setup(primary key(DATA_TYPE, STYLE, COLOR, size, SETUP_ORDER, ID))
Select * 
from
(select C.*, 
lag(Running_Inventory) over  (partition by  style, COLOR, size order by style, COLOR, size, DATE_ORDER) as Last_running_Inventory from
(select B.*, 
sum(QUANTITY) over (partition by  style, COLOR, size order by style, COLOR, size, DATE_ORDER, id) as Running_Inventory,
CASE WHEN sum(ORDER_QTY - Last_Quantity) over (partition by  style, COLOR, size order by style, COLOR, size, DATE_ORDER, id) <= 0 THEN 0 
ELSE sum(ORDER_QTY - Last_Quantity) over (partition by  style, COLOR, size order by style, COLOR, size, DATE_ORDER, id) END as Running_Sales,
sum(ORDER_QTY) over (partition by  style, COLOR, size order by style, COLOR, size, DATE_ORDER, id)  as Cumulative_Sales
from
(select A.*, 
row_number() over (partition by DATA_TYPE, style, COLOR, size order by style, COLOR, size, SETUP_ORDER) as ID,
 ifnull(lag(QUANTITY) over  (partition by  style, COLOR, size order by style, COLOR, size, DATE_ORDER),0) as Last_Quantity
from (
SELECT "Orders" as DATA_TYPE, STYLE, ifnull(COLOR,"") as COLOR ,NUMBER as Size_Order,  ifnull(SIZE,"") as Size, 
SIZE_RUN1 as ppk_qty,
case when style like "O-%" then "" else Size_Run end as Size_Run, 
case when style like "O-%" then "" else Size_Breakdown end as Size_Breakdown, 
case when style like "O-%" then "" else Pack_Breakdown end as Pack_Breakdown, 
Pack_Qty as PAIRS, concat(Size_Run," Total Case Pairs =", Pack_Qty) as CASE_DETAILS, 
"" as IMAGE,SHIP_DATE, 1 as DATE_ORDER, 1 as SETUP_ORDER, 
0 AS QUANTITY, (ORDER_QTY - INVOICED_QTY) as ORDER_QTY,
0 as RETAIL_PRS, UNIT_PRICE as WHOLE_PRS, 0 as PRICE_BASE, 0 as FRT_CUS, 0 as PROD_DUTY, 0 as AVG_COST
FROM open_order_data A 
left join case_breakdown B on A.CLASS_CODE = B.class_cd
UNION
SELECT 
DATA_TYPE, style, ifnull(COLOR,"") as COLOR, Size_Order, ifnull(SIZE,"") as Size, 
PPK_PACK,
case when style like "O-%" then "" else Size_Run end as Size_Run, 
case when style like "O-%" then "" else Size_Breakdown end as Size_Breakdown, 
case when style like "O-%" then "" else Pack_Breakdown end as Pack_Breakdown, 
PAIRS, CASE_DETAILS, IMAGE, DATE, 2 AS DATE_ORDER,  2 as SETUP_ORDER, 
greatest(QUANTITY,0) as QUANTITY, 0 as ORDER_QTY,
RETAIL_PRS, WHOLE_PRS, PRICE_BASE, FRT_CUS, PROD_DUTY, AVG_COST
FROM inventory_logic_by_size
union 
SELECT DATA_TYPE, style, ifnull(COLOR,"") as COLOR, Size_Order, ifnull(SIZE,"") as Size, 
PPK_QTY,
case when style like "O-%" then "" else Size_Run end as Size_Run, 
case when style like "O-%" then "" else Size_Breakdown end as Size_Breakdown, 
case when style like "O-%" then "" else Pack_Breakdown end as Pack_Breakdown,  
PAIRS, CASE_DETAILS, IMAGE_NM as IMAGE, DATE, 3 AS DATE_ORDER, 2 as SETUP_ORDER, 
PO_QTY as QUANTITY, 0 as ORDER_QTY,
RETAIL_PRS, WHOLE_PRS, PRICE_BASE, FRT_CUS, PROD_DUTY, AVG_COST
FROM po_logic_by_size_run 
) A) B)C) D;


drop table if exists inventory_detail;
create table if not exists inventory_detail(primary key(DATA_TYPE, STYLE, COLOR, size, SETUP_ORDER, ID))
select *, dense_rank() over(partition by core_style order by core_style_rank, color) as style_ranking from
(
select *,
case when style like 'O-%' then 2 else 1 end as core_style_rank,
case when style like 'O-%' then right(style,length(style)-2) else style end as core_style
from
(select A.* ,B.DESCRIPTION,
case when Running_Sales >= Running_Inventory then QUANTITY 
	when Running_Sales >= QUANTITY then QUANTITY
      when Running_Sales < Running_Inventory then Running_Sales
    end as Sales_Against_Qty,
case when Running_Sales >= Running_Inventory then 0 
	when Running_Sales >= QUANTITY then 0 
    when Running_Sales < Running_Inventory then QUANTITY - Running_Sales
    end as ATS    
from inventory_detail_setup A
left join (select STYLE, COLOR_CODE, COLOR, DESCRIPTION FROM style_master GROUP BY  STYLE,  COLOR ) B USING(STYLE, COLOR)
where SETUP_ORDER = 2
and QUANTITY > 0) A) B;


Alter table inventory_detail add column total_style_quantity int after QUANTITY;
Alter table inventory_detail add column cases int after total_style_quantity;

Alter table inventory_detail add column ats_total_style_quantity int after ATS;
Alter table inventory_detail add column ats_cases int after ats_total_style_quantity;


update inventory_detail set cases = QUANTITY / ppk_qty where size_run is not null and size_run != "";

update inventory_detail A inner join (
select STYLE, color, SHIP_DATE, sum(QUANTITY) as QUANTITY, min(cases) as cases
 from inventory_detail group by style, color, SHIP_DATE) B  using(style, color, SHIP_DATE)
set A.total_style_quantity = B.QUANTITY,
A.cases = B.cases
where  size_run is not null and size_run != "";

update inventory_detail set ats_cases = ATS / ppk_qty where size_run is not null and size_run != "";

update inventory_detail A inner join (
select STYLE, color, SHIP_DATE, sum(ATS) as QUANTITY, min(ats_cases) as cases
 from inventory_detail group by style, color, SHIP_DATE) B  using(style, color, SHIP_DATE)
set A.ats_total_style_quantity = B.QUANTITY,
A.ats_cases = B.cases
where  size_run is not null and size_run != "";
