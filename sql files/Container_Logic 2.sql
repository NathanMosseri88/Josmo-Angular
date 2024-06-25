-- ------------------------------------------------------------------
-- Set up Container Data
-- ------------------------------------------------------------------

drop table if exists containers;
create table if not exists containers(primary key(container_number))
select row_number() over (partition by "" order by container_number) as id, A.* from
(select distinct Container_Num as container_number, EST_DATE,EST_DATE + interval 2 week as ready_to_sell_date,  VENDOR as factory_name from po_data A
where Container_Num is not null
and Container_Num not in (
'NAVY ONLY HAVE 432 PRS... I CASE STOCK',
'NAVY',
'must look at original po for correct break down',
'LA IDEAL STORE 4',
'Initial Qty 720. Final Qty 702. Changed on 12/24/15                                                                     Packing List 15RLD082',
'Initial Qty 540. Final Qty 522. Changed on 12/24/15                                                                     Packing List 15RLD082',
'joey',
'add on 7/15/07 because was received and was not in any order',
'add in 7/15/2007 because was received and was not on order',
'original price 2.40 but with box, paper, handtag, and loose cargo charge.. price goes up to 2.90',
'taking all for Varity: Yvette 11/30/15',
'hello'
)
group by container_number
)A ;



-- -----------------------------------------------------------------------------------------
-- SIZE RUN ASSIGNED ORDERS-----------------------------------------------------------------
-- -----------------------------------------------------------------------------------------

update open_order_data set type = "No Size Run" where style in ("Logan", "8190");

drop table if exists order_size_run_check;
create table if not exists order_size_run_check(primary key(customer_ID, style, COLOR_CODE,RUN_CODE,CLASS_CODE, TOTAL_ORDER_QTY, ranking))
select *, row_number() over (partition by customer_ID, style, COLOR_CODE,RUN_CODE,CLASS_CODE, TOTAL_ORDER_QTY order by customer_ID, style, COLOR_CODE,RUN_CODE,CLASS_CODE,TOTAL_ORDER_QTY, ORDER_DATE) as Ranking   from
(select type, NT_Num as Order_Nt_Num, ORDER_DATE,SHIP_DATE,Cancel_date, ORDER_NUMBER,ifnull(customer_ID,"") as customer_ID, CUSTOMER, STYLE, COLOR_CODE,RUN_CODE, ifnull(CLASS_CODE,"") as CLASS_CODE, 
UNIT_PRICE, COST, SALES_ID, SALES_REP, 
TOTAL_ORDER_QTY, PREPACK_QTY,
case when PREPACK_QTY >0 then TOTAL_ORDER_QTY / PREPACK_QTY else TOTAL_ORDER_QTY end  as Case_Packs
from open_order_data A
where type = "Size Run"
group by ORDER_NUMBER,NT_Num,  CUSTOMER, STYLE, COLOR_CODE) A;

drop table if exists po_size_run_check;
create table if not exists po_size_run_check(primary key(customer_ID, style, COLOR_CODE,RUN_CODE,CLASS_CODE, TOTAL_ORDER_QTY, ranking))
select *, row_number() over (partition by customer_ID, style, COLOR_CODE,RUN_CODE,CLASS_CODE, TOTAL_ORDER_QTY order by customer_ID, style, COLOR_CODE,RUN_CODE,CLASS_CODE,TOTAL_ORDER_QTY, ORDER_DATE) as Ranking   from
(select type, NT_Num as PO_NT_Num, ORDER_DATE,EST_DATE, PUR_NUM, CUS_ID as customer_ID, ifnull(B.customer_name,"")as customer_name, STYLE, COLOR_CODE,ifnull(RUN_CD,"") as RUN_CODE, ifnull(CLASS_CD,"") as CLASS_CODE, Total_Order_Qty 
from po_data A
left join customers B on A.CUS_ID = B.CUSTOMER_ID
where  
type = "Size Run"
and Total_Receive_Qty < Total_Order_Qty
group by PUR_NUM, NT_Num, CUS_ID, STYLE, COLOR_CODE) A;



DROP TABLE if exists size_run_assigned_orders;
create table if not exists size_run_assigned_orders(primary key(customer_ID, style, COLOR_CODE,RUN_CODE,CLASS_CODE, TOTAL_ORDER_QTY, ranking))
select A.*, B.Order_Nt_Num,  B.ORDER_DATE AS SALE_ORDER_DATE, B.SHIP_DATE,B.Cancel_date,  B.ORDER_NUMBER, 
b.UNIT_PRICE, b.COST, b.SALES_ID, b.SALES_REP, 
b.TOTAL_ORDER_QTY AS ORDER_QTY, B.PREPACK_QTY, B.Case_Packs
from po_size_run_check A left join order_size_run_check B using(customer_ID, style, COLOR_CODE,RUN_CODE,CLASS_CODE, TOTAL_ORDER_QTY, ranking)
where B.type is not null;


-- -----------------------------------------------------------------------------------------
-- NO SIZE RUN ASSIGNED ORDERS -------------------------------------------------------------
-- -----------------------------------------------------------------------------------------

drop table if exists order_no_size_run_check;
create table if not exists order_no_size_run_check
select A.*, B.size_breakdown, B.order_breakdown,  
row_number() over (partition by customer_ID, style, COLOR_CODE,size, RUN_CODE,CLASS_CODE, ORDER_QTY,  B.size_breakdown, B.order_breakdown 
order by customer_ID, style, COLOR_CODE,RUN_CODE,CLASS_CODE,ORDER_QTY, ORDER_DATE,  B.size_breakdown, B.order_breakdown) as Ranking   from
(select type, NT_Num as Order_Nt_Num, ORDER_DATE,SHIP_DATE,Cancel_date, ORDER_NUMBER,customer_ID, CUSTOMER, STYLE, COLOR_CODE,ifnull(size,"") as size, RUN_CODE, ifnull(CLASS_CODE,"") as CLASS_CODE, 
UNIT_PRICE, COST, SALES_ID, SALES_REP, 
ORDER_QTY, PREPACK_QTY, 
ORDER_QTY as Case_Packs,
TOTAL_ORDER_QTY
from open_order_data A
where type = "No Size Run"
group by ORDER_NUMBER, NT_Num, CUSTOMER, STYLE, COLOR_CODE, size) A
left join 
(select type, NT_Num as Order_Nt_Num, ORDER_DATE,SHIP_DATE,Cancel_date, ORDER_NUMBER,customer_ID, CUSTOMER, STYLE, COLOR_CODE, RUN_CODE, ifnull(CLASS_CODE,"") as CLASS_CODE, 
ORDER_QTY, PREPACK_QTY, 
ifnull(group_concat(size order by size),"") as size_breakdown ,
ifnull(group_concat(round(Order_Qty,0) order by size),"") as order_breakdown , TOTAL_ORDER_QTY
from open_order_data A
where type = "No Size Run" 
group by ORDER_NUMBER, NT_Num, CUSTOMER, STYLE, COLOR_CODE) B using( ORDER_NUMBER, Order_Nt_Num, CUSTOMER, STYLE, COLOR_CODE);


Alter table order_no_size_run_check  modify size_breakdown varchar(255),
modify order_breakdown varchar(255);

update order_no_size_run_check set customer_ID = 0 where customer_ID is null;

Alter table order_no_size_run_check 
add primary key(customer_ID, style, COLOR_CODE,size, RUN_CODE,CLASS_CODE, ORDER_QTY, size_breakdown, order_breakdown, ranking);


drop table if exists po_no_size_run_check;
create table if not exists po_no_size_run_check
select A.*,B.size_breakdown, B.order_breakdown,
 row_number() over (partition by customer_ID, style, COLOR_CODE,size, RUN_CODE,CLASS_CODE, Order_Qty, B.size_breakdown, B.order_breakdown order by customer_ID, style, COLOR_CODE,size, RUN_CODE,CLASS_CODE,Order_Qty, ORDER_DATE, B.size_breakdown, B.order_breakdown) as Ranking   
 from
(select type, NT_Num as PO_Nt_Num, ORDER_DATE,EST_DATE, PUR_NUM, CUS_ID as customer_ID, ifnull(B.customer_name,"")as customer_name, STYLE, COLOR_CODE,ifnull(size,"") as size, ifnull(RUN_CD,"") as RUN_CODE, ifnull(CLASS_CD,"") as CLASS_CODE, 
Order_Qty , TOTAL_ORDER_QTY
from po_data A
left join customers B on A.CUS_ID = B.CUSTOMER_ID
where  
type = "No Size Run" 
and Total_Receive_Qty < Total_Order_Qty
group by PUR_NUM,NT_Num,  CUS_ID, STYLE, COLOR_CODE, size) A
left join (select type, NT_Num as PO_Nt_Num, ORDER_DATE,EST_DATE, PUR_NUM, CUS_ID as customer_ID,
ifnull(B.customer_name,"")as customer_name, STYLE, COLOR_CODE, ifnull(RUN_CD,"") as RUN_CODE, ifnull(CLASS_CD,"") as CLASS_CODE, 
ifnull(group_concat(size order by size),"") as size_breakdown ,
ifnull(group_concat(round(Order_Qty,0) order by size),"") as order_breakdown , TOTAL_ORDER_QTY
from po_data A
left join customers B on A.CUS_ID = B.CUSTOMER_ID
where  
type = "No Size Run" and Total_Receive_Qty < Total_Order_Qty
group by PUR_NUM,NT_Num,  CUS_ID, STYLE, COLOR_CODe) B  using(PUR_NUM, PO_Nt_Num, customer_ID, STYLE, COLOR_CODE);

Alter table po_no_size_run_check  modify size_breakdown varchar(100),
modify order_breakdown varchar(100);
Alter table po_no_size_run_check 
add primary key(customer_ID, style, COLOR_CODE,size, RUN_CODE,CLASS_CODE, ORDER_QTY, size_breakdown, order_breakdown, ranking);


DROP TABLE if exists no_size_run_assigned_orders;
create table if not exists no_size_run_assigned_orders(primary key(customer_ID, style, COLOR_CODE,size, RUN_CODE,CLASS_CODE, size_breakdown, order_breakdown, Order_Qty, ranking))
select A.*, B.Order_Nt_Num, B.ORDER_DATE AS SALE_ORDER_DATE, B.SHIP_DATE,B.Cancel_date,  UNIT_PRICE, COST, SALES_ID, SALES_REP, 
B.ORDER_NUMBER, b.Order_Qty as Order_Qty_detail, B.PREPACK_QTY, B.Case_Packs
from po_no_size_run_check A left join order_no_size_run_check B using(customer_ID, style, COLOR_CODE,size, RUN_CODE,CLASS_CODE, Order_Qty,size_breakdown,order_breakdown ,  ranking)
where B.type is not null;

-- -----------------------------------------------------------------------------------------
-- INVENTORY PACKS -------------------------------------------------------------------------
-- -----------------------------------------------------------------------------------------

drop table if exists inventory_packs;
create table if not exists inventory_packs(primary key(prod_cd, prod_clr))
select  PROD_CD, PROD_CLR, SZ_RUN, CLASS_CD, PAIRS, `INVENTORY_QTY.1` as Total_INVENTORY_QTY,
case when SZ_RUN != "X" and `INVENTORY_QTY.1` >0 and PAIRS >0 then round(`INVENTORY_QTY.1`/PAIRS - mod( `INVENTORY_QTY.1`/PAIRS, 1),0)  else 0 end  as Style_Color_Packs,   
 min(Unit_Packs) as Unit_Packs from
(select PROD_CD, PROD_CLR,Size_Breakdown, SZ_RUN, CLASS_CD, PAIRS, INVENTORY_QTY, `INVENTORY_QTY.1`,
case when SZ_RUN != "X" and INVENTORY_QTY >0 and Size_Pack_Qty >0 and PROD_CD not in ("Logan", "8190")  then round(INVENTORY_QTY/Size_Pack_Qty - mod( INVENTORY_QTY/Size_Pack_Qty, 1),0) else 0 end as Unit_Packs
from inventory_data ) A
group by PROD_CD, PROD_CLR;


drop table if exists po_packs;
create table if not exists po_packs(primary key(PUR_NUM, STYLE, COLOR_CODE, NT_Num))
select PUR_NUM,NT_NUM, ORDER_DATE, EST_DATE, RUN_CD, CLASS_CD, STYLE, COLOR_CODE, PREPACK_QTY, Total_Order_Qty, 
count(distinct  PUR_NUM, STYLE, COLOR_CODE, ORDER_DATE, Total_Order_Qty) as unique_orders,
case when Type = "Size Run" and Total_Order_Qty >0 and PREPACK_QTY >0 and style not in ("Logan", "8190")  then round(Total_Order_Qty/PREPACK_QTY - mod( Total_Order_Qty/PREPACK_QTY, 1),0) else 0 end as Unit_Packs
from po_data 
WHERE Type = "Size Run" 
AND Total_Receive_Qty < Total_Order_Qty
group by PUR_NUM, STYLE, COLOR_CODE, NT_NUM;

drop table if exists po_no_packs;
create table if not exists po_no_packs(primary key(PUR_NUM, STYLE, COLOR_CODE, NT_Num))
select PUR_NUM,NT_NUM, ORDER_DATE, EST_DATE, RUN_CD, CLASS_CD, STYLE, COLOR_CODE, 0 as PREPACK_QTY, Total_Order_Qty, 
count(distinct  PUR_NUM, STYLE, COLOR_CODE, ORDER_DATE, Total_Order_Qty) as unique_orders,
case when Type = "No Size Run" and Total_Order_Qty >0 and PREPACK_QTY >0 and style not in ("Logan", "8190")  then round(Total_Order_Qty - mod( Total_Order_Qty, 1),0) else 0 end as Unit_Packs
from po_data 
WHERE Type = "No Size Run" 
AND Total_Receive_Qty < Total_Order_Qty
group by PUR_NUM, STYLE, COLOR_CODE, NT_NUM;




drop table if exists so_packs;
create table if not exists so_packs(primary key(ORDER_NUMBER, STYLE, COLOR_CODE, NT_Num))
select ORDER_NUMBER,NT_Num, ORDER_DATE, SHIP_DATE, RUN_CODE, CLASS_CODE, STYLE, COLOR_CODE, PREPACK_QTY, Total_Order_Qty, TOTAL_INVOICED_QTY, 
count(distinct  concat(ORDER_NUMBER, STYLE, COLOR_CODE, ORDER_DATE, Total_Order_Qty, NT_Num)) as unique_orders,
case when Type = "Size Run" and Total_Order_Qty >0   then round(Total_Order_Qty/(case when PREPACK_QTY = 0 then 1 else PREPACK_QTY end) - mod( Total_Order_Qty/(case when PREPACK_QTY = 0 then 1 else PREPACK_QTY end), 1),0) else 0 end as Unit_Packs
from open_order_data 
WHERE Type = "Size Run" 
AND TOTAL_INVOICED_QTY < Total_Order_Qty
group by ORDER_NUMBER, STYLE, COLOR_CODE, NT_Num;


drop table if exists container_inventory_setup;
create table if not exists container_inventory_setup(primary key(style, color_code, size))
select 
"Inventory" as Type,
case when A.SZ_RUN = "X" then "No Size Run" else "Size Run" end as Size_Run,
"Stock",
1 as order_number,
curdate() as date,
null as ORDER_DATE,
null as cancel_date,
"" as Nt_Num,
A.prod_cd as style, 
A.PROD_CLR as color_code,
B.CLR_DESC as color,
A.SZ_RUN,
A.SZ_RUN as RUN_CD,
A.CLASS_CD, 
A.PAIRS as PREPACK_QTY,
A.NUMBER,
A.Size_Breakdown as Size,
A.Size_Pack_Qty,
"Inventory" as Container,
A.UPC_CD as UPC,
A.Image, 
A.PRICE_BASE,
A.FRT_CUS,
A.HNDL_FEE,
A.PROD_DUTY,
A.AVG_COST,
A.INVENTORY_QTY as QTY,
A.`INVENTORY_QTY.1` as Total_Pack_Qty,
C.Unit_Packs,
C.Unit_Packs * A.Size_Pack_Qty as Size_Run_Qty,
A.INVENTORY_QTY - (C.Unit_Packs * A.Size_Pack_Qty) as No_Size_Run_Qty
from inventory_data A
left join color_codes  B USING(PROD_CLR)
left join inventory_packs C using(prod_cd, prod_clr)
group by style, color_code, size;

create index date_style_color_code_size on container_inventory_setup(date, style, color_code, size);

drop table if exists container_po_setup;
create table if not exists container_po_setup
select 
"Purchase Order" as Type,
Type as Size_Run,
A.VENDOR,
A.PUR_NUM as order_number,
A.EST_DATE + interval 14 day as date,
A.ORDER_DATE,
null as Cancel_Date,
A.Nt_Num,
A.STYLE,
A.COLOR_CODE,
A.color, 
c.SZ_RUN,
A.RUN_CD,
A.CLASS_CD,
E.Size_Breakdown,
E.Pack_Breakdown,
E.Size_Run as Size_Run_Detail,
a.PREPACK_QTY,
A.NUMBER, 
A.Size,
c.Size_Pack_Qty,
A.Container_Num as Container,
c.UPC_CD as UPC,
c.Image, 
a.Unit_Cost as PRICE_BASE,
c.FRT_CUS,
c.HNDL_FEE,
c.PROD_DUTY,
c.AVG_COST,
round(A.Order_Qty,0) as QTY,
case when type = "Size Run" then  ifnull(D.Total_Order_Qty,  A.Total_Order_Qty)
	when type = "No Size Run" then  ifnull(DD.Total_Order_Qty,  A.Total_Order_Qty)
    end as Total_Pack_Qty, 
case when type = "Size Run" then  ifnull(D.Unit_Packs,  A.Total_Order_Qty)
	when type = "No Size Run" then  ifnull(DD.Unit_Packs,  A.Total_Order_Qty)
    end as Unit_Packs, 
case when type = "Size Run" then A.Order_Qty else 0 end as size_Run_Qty ,
case when type = "No Size Run" then A.Order_Qty else 0 end as no_size_Run_Qty 
from po_data A
left join containers B on A.Container_Num = B.container_number
left join inventory_data C on A.STYLE = C.PROD_CD and A.COLOR_CODE = C.PROD_CLR AND A.SIZE = c.Size_Breakdown
left join po_packs D on A.PUR_NUM = D.PUR_NUM and  A.style = D.style and A.COLOR_CODE = D.COLOR_CODE and A.Nt_Num = D.Nt_Num
left join po_no_packs DD on A.PUR_NUM = DD.PUR_NUM and  A.style = DD.style and A.COLOR_CODE = DD.COLOR_CODE and A.Nt_Num = DD.Nt_Num
left join case_breakdown E on A.class_cd = E.class_cd and A.RUN_CD = E.inv_sz
where
A.Total_Receive_Qty < A.Total_Order_Qty
order by A.Style, A.color, A.size, A.Nt_Num;

update container_po_setup A left join (
select style, color, image from container_po_setup where image is not  null group by style, color) B using(style, color)
set A.image = B.image where A.image is null;


drop table if exists container_so_setup;
create table if not exists container_so_setup
SELECT 
"Sales Order" as Type,
A.Type as Size_Run_Detail,
A.CUSTOMER_ID,
A.CUSTOMER, 
A.ORDER_NUMBER,
A.NT_Num, 
greatest(curdate(),A.ship_DATE) as date,
A.ORDER_DATE as order_date,
A.Cancel_Date,
A.style, 
A.color_code,
A.color,
A.RUN_CODE,
A.CLASS_CODE,
A.Sales_Id,
A.Sales_rep,
A.PREPACK_QTY,
A.NUMBER, 
A.size,
A.SIZE_RUN1 as Size_Run_Qty,
null as container,
C.UPC_CD as UPC,
C.Image, 
A.COST as PRICE_BASE,
C.FRT_CUS,
C.HNDL_FEE,
C.PROD_DUTY,
C.AVG_COST,
A.UNIT_PRICE, 
round(A.ORDER_QTY - A.INVOICED_QTY,0) as qty,
A.TOTAL_ORDER_QTY as Total_Pack_Qty,
case when A.type = "Size Run" then D.Unit_Packs else null end as Unit_Packs
FROM open_order_data A
left join inventory_data C on A.STYLE = C.PROD_CD and A.COLOR_CODE = C.PROD_CLR AND A.SIZE = c.Size_Breakdown
left join so_packs D on A.order_number = d.ORDER_NUMBER and A.ORDER_DATE = D.ORDER_DATE and A.style = D.style and A.COLOR_CODE = D.COLOR_CODE and A.NT_Num = D.NT_Num ;



alter table container_inventory_setup modify order_date date,
modify cancel_date date,
modify Container varchar(255);

alter table container_po_setup modify order_date date,
modify cancel_date date,
modify Container varchar(255);

alter table container_so_setup modify order_date date,
modify cancel_date date,
modify Container varchar(255);

drop table if exists container_order_detail_size_run;
create table if not exists container_order_detail_size_run(primary key (style, color_code, size))
select A.Size_Run_Detail, A.style, A.color_code,ifnull(A.size,"") as size , A.PREPACK_QTY, 
	sum(A.qty) as Qty, round(sum(A.Total_Pack_Qty) / A.PREPACK_QTY,0) as unit_cases,
	sum(case when b.ORDER_NUMBER is null then A.qty else null end) as Unassigned_Qty,
	ifnull(round(sum(case when b.ORDER_NUMBER is null then A.Total_Pack_Qty else null end)/A.PREPACK_QTY,0),0)  as Unassigned_Unit_Packs,
	sum(case when b.ORDER_NUMBER is not null then A.qty else null end) as Assigned_Qty,
    ifnull(round(sum(case when b.ORDER_NUMBER is not null then A.Total_Pack_Qty else null end)/A.PREPACK_QTY,0),0)  as Assigned_Unit_Packs
	from container_so_setup A 
    left join size_run_assigned_orders B on A.ORDER_NUMBER = B.ORDER_NUMBER and A.STYLE = B.STYLE and A.COLOR_CODE = B.COLOR_CODE  and A.NT_Num = B.Order_Nt_Num
	where A.Size_Run_Detail = "Size Run"
	group by A.style, A.color_code, A.size;
    
    drop table if exists conatiner_order_detail_no_size_run;
create table if not exists conatiner_order_detail_no_size_run(primary key (style, color_code, size))
select A.Size_Run_Detail, A.style, A.color_code,ifnull(A.size,"") as size , A.PREPACK_QTY, 
	sum(A.qty) as Qty, sum(A.qty) as unit_cases,
	sum(case when b.ORDER_NUMBER is null then A.qty else null end) as Unassigned_Qty,
	sum(case when b.ORDER_NUMBER is null then A.qty else null end)  as Unassigned_Unit_Packs,
	sum(case when b.ORDER_NUMBER is not null then A.qty else null end) as Assigned_Qty,
    sum(case when b.ORDER_NUMBER is not null then A.qty else null end)  as Assigned_Unit_Packs
	from container_so_setup A 
    left join no_size_run_assigned_orders B on A.ORDER_NUMBER = B.ORDER_NUMBER and A.STYLE = B.STYLE and A.COLOR_CODE = B.COLOR_CODE  and A.NT_Num = B.Order_Nt_Num and A.size = B.size
	where A.Size_Run_Detail = "No Size Run"
	group by A.style, A.color_code, A.size;
    
    
update container_po_setup  set size = "" where size is null;
update container_order_detail_size_run set size = "" where size is null;
update conatiner_order_detail_no_size_run set size = "" where size is null;

create index style_color_size on container_po_setup(style, color_code, size);

drop table if exists container_purchase_order_planning;
create table if not exists container_purchase_order_planning
select A.*, B.QTY as Inventory_Qty, B.Size_Run_Qty as Inventory_Size_Run_Qty, B.No_Size_Run_Qty as Inventory_No_Size_Run_Qty,
C.Qty as All_WIP, C.Qty - A.Qty as Other_PO_QTY, round(C.size_Run_Qty - A.size_Run_Qty,0) as Other_Size_Run_Qty,  round(C.no_size_Run_Qty - A.no_size_Run_Qty,0) as Other_No_Size_Run_Qty,
case when  A.Size_Run = "Size Run" then D.ORDER_NUMBER else DE.ORDER_NUMBER end as Assigned_Order_Number,
case when  A.Size_Run = "Size Run" then D.customer_ID  else DE.customer_ID end as customer_ID,
case when  A.Size_Run = "Size Run" then D.customer_name else DE.customer_name end as customer_name,
case when  A.Size_Run = "Size Run" then D.SALE_ORDER_DATE else DE.SALE_ORDER_DATE end as SALE_ORDER_DATE,
case when  A.Size_Run = "Size Run" then D.SHIP_DATE  else DE.SHIP_DATE end as SHIP_DATE,
case when  A.Size_Run = "Size Run" then D.Cancel_date else DE.Cancel_date end as Order_Cancel_date,
case when  A.Size_Run = "Size Run" then D.ORDER_QTY else A.QTY end as ORDER_QTY,
case when  A.Size_Run = "Size Run" then D.PREPACK_QTY else 0 end AS Order_Prepack,
case when  A.Size_Run = "Size Run" then D.CASE_PACKS else A.QTY end as CASE_PACKS,
case when  A.Size_Run = "Size Run" then D.UNIT_PRICE  else DE.UNIT_PRICE end as UNIT_PRICE,
case when  A.Size_Run = "Size Run" then D.COST  else DE.COST end as COST,
case when  A.Size_Run = "Size Run" then D.SALES_ID  else DE.SALES_ID end as SALES_ID,
case when  A.Size_Run = "Size Run" then D.SALES_REP  else DE.SALES_REP end as SALES_REP,
case when A.Size_Run = "Size Run" then E.Unassigned_Qty else F.Unassigned_Qty end as Unassigned_Qty,
case when A.Size_Run = "Size Run" then E.Unassigned_Unit_Packs else F.Unassigned_Unit_Packs end as Unassigned_Unit_Packs,
case when A.Size_Run = "Size Run" then E.Assigned_Qty else F.Assigned_Qty end as Assigned_Qty,
case when A.Size_Run = "Size Run" then E.Assigned_Unit_Packs else F.Assigned_Unit_Packs end as Assigned_Unit_Packs 
from container_po_setup A 
left join container_inventory_setup B on A.style = B.style and A.color_code = B.color_code and A.size = B.size
left join (select Size_Run, STYLE, color_code, Size, round(sum(QTY),0) as QTY, round(sum(size_Run_Qty),0) as size_Run_Qty, round(sum(no_size_Run_Qty),0) as no_size_Run_Qty 
from container_po_setup group by Size_Run, STYLE, color_code, Size) C on A.Size_Run = C.Size_Run and  A.style = C.style and A.color_code = C.color_code and A.size = C.size
left join size_run_assigned_orders D on A.Order_Number = D.PUR_NUM and A.NT_Num = D.PO_NT_Num and A.STYLE = D.STYLE and A.COLOR_CODE = D.COLOR_CODE
left join no_size_run_assigned_orders DE on A.Order_Number = DE.PUR_NUM and A.NT_Num = DE.PO_NT_Num and A.STYLE = DE.STYLE and A.COLOR_CODE = DE.COLOR_CODE And A.size = DE.Size
left join container_order_detail_size_run E on A.Size_Run = E.Size_Run_Detail and  A.STYLE = E.STYLE and A.COLOR_CODE = E.COLOR_CODE and A.size = E.size
left join conatiner_order_detail_no_size_run F  on A.Size_Run = F.Size_Run_Detail and  A.STYLE = F.STYLE and A.COLOR_CODE = F.COLOR_CODE and A.size = F.size;
-- where A.style = "CH92273" and A.COLOR_CODE = "NVRD";





#Step 1: Size Run Assigned - With Container X
#Step 2: Size Run UnAssigned - With Container X
#Step 3: Size Run Assigned - Without Container
#Step 4: Size Run UnAssigned - Without Container
#Step 5: no Size Run Assigned- With Container
#Step 6: no Size Run UnAssigned- With Container
#Step 7: no Size Run Assigned- Without Container
#Step 8: no Size Run UnAssigned- Without Container

drop table if exists container_size_run_assigned_with_container;
create table if not exists container_size_run_assigned_with_container
select 
Container, Size_Run, "Make Up" as Assigned,
STYLE, COLOR_CODE, color, 
"" as Number,
"" as Size,
Size_Breakdown, 
Pack_Breakdown, 
Size_Run_Detail,
count(distinct order_number) as PO_Count,
group_concat(distinct order_number) as Po_Numbers,
"" as Nt_Num, 
date as EST_Date,
Order_Date,
AVG_COST, 
PREPACK_QTY,
Total_Pack_Qty,
round(Total_Pack_Qty / PREPACK_QTY,0) as Cases,
sum(Inventory_Size_Run_Qty) as Inventory_Size_Run_Qty,
sum(Other_Size_Run_Qty) as Other_Size_Run_Qty,
SUM(Unassigned_Qty) AS Unassigned_Orders_Qty,
Unassigned_Unit_Packs as Unassigned_Orders_Packs,
SUM(Assigned_Qty) as Assigned_Orders_Qty, 
Assigned_Unit_Packs as Assigned_Orders_Packs,
UNIT_PRICE,
SALES_ID,
SALES_REP,
Assigned_Order_Number,
customer_ID,
customer_name,
SALE_ORDER_DATE,
SHIP_DATE,
Cancel_date,
ORDER_QTY,
Order_Prepack, 
CASE_PACKS
from container_purchase_order_planning
where Size_Run = "Size Run"
and Container  is not null
and Assigned_Order_Number is not null
group by Container,order_number, STYLE, COLOR_CODE;

drop table if exists container_size_run_assigned_without_container;
create table if not exists container_size_run_assigned_without_container
select 
Container, Size_Run, "Make Up" as Assigned,
STYLE, COLOR_CODE, color, 
"" as Number,
"" as Size,
Size_Breakdown, 
Pack_Breakdown, 
Size_Run_Detail,
count(distinct order_number) as PO_Count,
group_concat(distinct order_number) as Po_Numbers,
"" as Nt_Num, 
date as EST_Date,
Order_Date,
AVG_COST,
PREPACK_QTY,
Total_Pack_Qty,
round(Total_Pack_Qty / PREPACK_QTY,0) as Cases,
sum(Inventory_Size_Run_Qty) as Inventory_Size_Run_Qty,
sum(Other_Size_Run_Qty) as Other_Size_Run_Qty,
sum(Unassigned_Qty) AS Unassigned_Orders_Qty,
Unassigned_Unit_Packs as Unassigned_Orders_Packs,
sum(Assigned_Qty) as Assigned_Orders_Qty, 
Assigned_Unit_Packs as Assigned_Orders_Packs,
UNIT_PRICE,
SALES_ID,
SALES_REP,
Assigned_Order_Number,
customer_ID,
customer_name,
SALE_ORDER_DATE,
SHIP_DATE,
Cancel_date,
ORDER_QTY,
Order_Prepack, 
CASE_PACKS
from container_purchase_order_planning
where Size_Run = "Size Run"
and Container  is null
and Assigned_Order_Number is not null
group by order_number, STYLE, COLOR_CODE;

drop table if exists container_size_run_unassigned_with_container;
create table if not exists container_size_run_unassigned_with_container
select A.*,
B.UNIT_PRICE,
B.SALES_ID,
B.SALES_REP,
B.ORDER_NUMBER,
B.customer_ID,
B.CUSTOMER,
B.order_date as SALE_ORDER_DATE,
B.date as SHIP_DATE,
B.Cancel_Date,
B.Total_Pack_Qty as ORDER_QTY,
B.PREPACK_QTY as Order_Prepack,
B.Unit_Packs as case_packs
from
(select 
A.Container, A.Size_Run,"Stock",
A.STYLE, A.COLOR_CODE, A.color,
"" as Number,
"" as Size,
Size_Breakdown, 
Pack_Breakdown, 
Size_Run_Detail,
count(distinct A.order_number) as PO_Count,
group_concat(distinct A.order_number) as Po_Numbers,
"" as Nt_Num,
date as EST_Date,
Order_Date,
AVG_COST,  
PREPACK_QTY,
A.Total_Pack_Qty,
round(A.Total_Pack_Qty / A.PREPACK_QTY,0) as Cases,
sum(Inventory_Size_Run_Qty) as Inventory_Size_Run_Qty,
sum(Other_Size_Run_Qty) as Other_Size_Run_Qty,
sum(Unassigned_Qty) AS Unassigned_Orders_Qty,
Unassigned_Unit_Packs as Unassigned_Orders_Packs,
sum(Assigned_Qty) as Assigned_Orders_Qty, 
Assigned_Unit_Packs as Assigned_Orders_Packs
from container_purchase_order_planning A
where Size_Run = "Size Run"
and Container  is not null
and Assigned_Order_Number is null
group by A.Container, A.STYLE, A.COLOR_CODE) A 
left join (select A.style, A.color_code,A.color,  A.ORDER_NUMBER, A.CUSTOMER_id, A.CUSTOMER, A.date, A.order_date, A.Cancel_Date, A.PREPACK_QTY, A.Total_Pack_Qty, A.Unit_Packs, A.AVG_COST, A.UNIT_PRICE ,
		A.SALES_ID, A.SALES_Rep
		from container_so_setup A 
		left join size_run_assigned_orders B on A.Order_Number = B.Order_Number and A.NT_Num = B.order_NT_Num and A.STYLE = B.STYLE and A.COLOR_CODE = B.COLOR_CODE
		where Size_Run_Detail = "Size Run"
        and B.type is  null
        group by  A.style, A.color_code,A.ORDER_NUMBER
        ) B on A.style = B.style and A.color_code = B.color_code;
        
drop table if exists container_size_run_unassigned_without_container;
create table if not exists container_size_run_unassigned_without_container
select A.*,
B.UNIT_PRICE,
B.SALES_ID,
B.SALES_REP,
B.ORDER_NUMBER,
B.customer_ID,
B.CUSTOMER,
B.order_date as SALE_ORDER_DATE,
B.date as SHIP_DATE,
B.Cancel_Date,
B.Total_Pack_Qty as ORDER_QTY,
B.PREPACK_QTY as Order_Prepack,
B.Unit_Packs as case_packs
from
(select 
A.Container, A.Size_Run,"Stock",
A.STYLE, A.COLOR_CODE, A.color,
"" as Number,
"" as Size,
Size_Breakdown, 
Pack_Breakdown, 
Size_Run_Detail,
count(distinct A.order_number) as PO_Count,
group_concat(distinct A.order_number) as Po_Numbers,
"" as Nt_Num, 
date as EST_Date,
Order_Date,
AVG_COST, 
PREPACK_QTY,
A.Total_Pack_Qty,
round(A.Total_Pack_Qty / A.PREPACK_QTY,0) as Cases,
sum(Inventory_Size_Run_Qty) as Inventory_Size_Run_Qty,
sum(Other_Size_Run_Qty) as Other_Size_Run_Qty,
sum(Unassigned_Qty) AS Unassigned_Orders_Qty,
Unassigned_Unit_Packs as Unassigned_Orders_Packs,
sum(Assigned_Qty) as Assigned_Orders_Qty, 
Assigned_Unit_Packs as Assigned_Orders_Packs
from container_purchase_order_planning A
where Size_Run = "Size Run"
and Container  is null
and Assigned_Order_Number is null
group by A.order_number, A.STYLE, A.COLOR_CODE) A 
left join (select A.style, A.color_code,A.color,  A.ORDER_NUMBER, A.CUSTOMER_id, A.CUSTOMER, A.date, A.order_date, A.Cancel_Date, A.PREPACK_QTY, A.Total_Pack_Qty, A.Unit_Packs, A.AVG_COST, A.UNIT_PRICE ,
		A.SALES_ID, A.SALES_Rep
		from container_so_setup A 
		left join size_run_assigned_orders B on A.Order_Number = B.Order_Number and A.NT_Num = B.order_NT_Num and A.STYLE = B.STYLE and A.COLOR_CODE = B.COLOR_CODE
		where Size_Run_Detail = "Size Run"
        and B.type is  null
        group by  A.style, A.color_code,A.ORDER_NUMBER
        ) B on A.style = B.style and A.color_code = B.color_code;
        
-- -------------------------------------------------------------------------------------------------
-- -------------------------------------------------------------------------------------------------
-- -------------------------------------------------------------------------------------------------


drop table if exists container_no_size_run_assigned_with_container;
create table if not exists container_no_size_run_assigned_with_container
select 
Container, Size_Run, "Make Up" as Assigned,
STYLE, COLOR_CODE, color, 
Number,
size,
"" as Size_Breakdown, 
"" as Pack_Breakdown, 
size as Size_Run_Detail,
1 as PO_Count,
order_number as Po_Numbers,
Nt_Num, 
date as EST_Date,
Order_Date,
AVG_COST, 
0 as PREPACK_QTY,
QTY as Total_Pack_Qty,
QTY as Cases,
sum(Inventory_No_Size_Run_Qty) as Inventory_Size_Run_Qty,
sum(Other_No_Size_Run_Qty) as Other_Size_Run_Qty,
SUM(Unassigned_Qty) AS Unassigned_Orders_Qty,
SUM(Unassigned_Unit_Packs) as Unassigned_Orders_Packs,
SUM(Assigned_Qty) as Assigned_Orders_Qty, 
SUM(Assigned_Unit_Packs) as Assigned_Orders_Packs,
UNIT_PRICE,
SALES_ID,
SALES_REP,
Assigned_Order_Number,
customer_ID,
customer_name,
SALE_ORDER_DATE,
SHIP_DATE,
Cancel_date,
ORDER_QTY,
Order_Prepack, 
CASE_PACKS
from container_purchase_order_planning
where Size_Run = "No Size Run"
and Container  is not null
and Assigned_Order_Number is not null
group by Container,order_number,Nt_Num,  STYLE, COLOR_CODE, Size;


drop table if exists container_no_size_run_assigned_without_container;
create table if not exists container_no_size_run_assigned_without_container
select 
Container, Size_Run, "Make Up" as Assigned,
STYLE, COLOR_CODE, color, 
Number,
size,
"" as Size_Breakdown, 
"" as Pack_Breakdown, 
size as Size_Run_Detail,
1 as PO_Count,
order_number as Po_Numbers,
Nt_Num, 
date as EST_Date,
Order_Date,
AVG_COST, 
0 as PREPACK_QTY,
QTY as Total_Pack_Qty,
QTY as Cases,
sum(Inventory_No_Size_Run_Qty) as Inventory_Size_Run_Qty,
sum(Other_No_Size_Run_Qty) as Other_Size_Run_Qty,
SUM(Unassigned_Qty) AS Unassigned_Orders_Qty,
SUM(Unassigned_Unit_Packs) as Unassigned_Orders_Packs,
SUM(Assigned_Qty) as Assigned_Orders_Qty, 
SUM(Assigned_Unit_Packs) as Assigned_Orders_Packs,
UNIT_PRICE,
SALES_ID,
SALES_REP,
Assigned_Order_Number,
customer_ID,
customer_name,
SALE_ORDER_DATE,
SHIP_DATE,
Cancel_date,
ORDER_QTY,
Order_Prepack, 
CASE_PACKS
from container_purchase_order_planning
where Size_Run = "No Size Run"
and Container  is  null
and Assigned_Order_Number is not null
group by order_number, Nt_Num, STYLE, COLOR_CODE, Size;


drop table if exists container_no_size_run_unassigned_with_container;
create table if not exists container_no_size_run_unassigned_with_container
select A.*,
B.UNIT_PRICE,
B.SALES_ID,
B.SALES_REP,
B.ORDER_NUMBER,
B.customer_ID,
B.CUSTOMER,
B.order_date as SALE_ORDER_DATE,
B.date as SHIP_DATE,
B.Cancel_Date,
B.qty as ORDER_QTY,
0 as Order_Prepack,
B.qty as case_packs
from
(select 
A.Container, A.Size_Run,"Stock",
A.STYLE, A.COLOR_CODE, A.color,
Number,
Size,
"" as Size_Breakdown, 
"" as Pack_Breakdown, 
Size as Size_Run_Detail,
count(distinct A.order_number) as PO_Count,
group_concat(distinct A.order_number) as Po_Numbers,
"" as Nt_Num, 
date as EST_Date,
Order_Date,
AVG_COST, 
0 as PREPACK_QTY,
A.qty as Total_Pack_Qty,
A.qty as Cases,
sum(Inventory_No_Size_Run_Qty) as Inventory_Size_Run_Qty,
sum(Other_No_Size_Run_Qty) as Other_Size_Run_Qty,
sum(Unassigned_Qty) AS Unassigned_Orders_Qty,
Unassigned_Unit_Packs as Unassigned_Orders_Packs,
sum(Assigned_Qty) as Assigned_Orders_Qty, 
Assigned_Unit_Packs as Assigned_Orders_Packs
from container_purchase_order_planning A
where Size_Run = "No Size Run"
and Container  is not null
and Assigned_Order_Number is null
group by A.Container, A.STYLE, A.COLOR_CODE, A.Size) A 
left join (select A.style, A.color_code,A.color,A.size, A.ORDER_NUMBER, A.CUSTOMER_id, A.CUSTOMER, A.date, A.order_date, A.Cancel_Date, A.PREPACK_QTY, A.qty, A.Total_Pack_Qty, A.Unit_Packs, A.AVG_COST, A.UNIT_PRICE ,
	A.SALES_ID,A.SALES_REP, B.type
		from container_so_setup A 
		left join no_size_run_assigned_orders B on A.Order_Number = B.Order_Number and A.NT_Num = B.order_NT_Num and A.STYLE = B.STYLE and A.COLOR_CODE = B.COLOR_CODE and A.Size = B.size
		where Size_Run_Detail = "No Size Run"
        and B.type is  null
        group by  A.style, A.color_code,A.size, A.ORDER_NUMBER, A.NT_Num
        ) B on A.style = B.style and A.color_code = B.color_code and A.size = B.size;
        


drop table if exists container_no_size_run_unassigned_without_container;
create table if not exists container_no_size_run_unassigned_without_container
select A.*,
B.UNIT_PRICE,
B.SALES_ID,
B.SALES_REP,
B.ORDER_NUMBER,
B.customer_ID,
B.CUSTOMER,
B.order_date as SALE_ORDER_DATE,
B.date as SHIP_DATE,
B.Cancel_Date,
B.qty as ORDER_QTY,
0 as Order_Prepack,
B.qty as case_packs
from
(select 
A.Container, A.Size_Run,"Stock",
A.STYLE, A.COLOR_CODE, A.color,
Number,
Size,
"" as Size_Breakdown, 
"" as Pack_Breakdown, 
Size as Size_Run_Detail,
1 as PO_Count,
order_number as Po_Numbers,
group_concat(Nt_Num order by nt_num) as Nt_Num, 
date as EST_Date,
Order_Date,
AVG_COST, 
0 as PREPACK_QTY,
sum(A.qty) as Total_Pack_Qty,
sum(A.qty) as Cases,
sum(Inventory_No_Size_Run_Qty) as Inventory_Size_Run_Qty,
sum(Other_No_Size_Run_Qty) as Other_Size_Run_Qty,
sum(Unassigned_Qty) AS Unassigned_Orders_Qty,
Unassigned_Unit_Packs as Unassigned_Orders_Packs,
sum(Assigned_Qty) as Assigned_Orders_Qty, 
Assigned_Unit_Packs as Assigned_Orders_Packs
from container_purchase_order_planning A
where Size_Run = "No Size Run"
and Container  is  null
and Assigned_Order_Number is null
group by A.order_number, A.STYLE, A.COLOR_CODE, A.Size) A 
left join (select A.style, A.color_code,A.color,A.size, A.ORDER_NUMBER, A.CUSTOMER_id, A.CUSTOMER, A.date, A.order_date, A.Cancel_Date, A.PREPACK_QTY, A.qty, A.Total_Pack_Qty, A.Unit_Packs, A.AVG_COST, A.UNIT_PRICE ,
      A.SALES_ID,A.SALES_REP, B.type
		from container_so_setup A 
		left join no_size_run_assigned_orders B on A.Order_Number = B.Order_Number and A.NT_Num = B.order_NT_Num and A.STYLE = B.STYLE and A.COLOR_CODE = B.COLOR_CODE and A.Size = B.size
		where Size_Run_Detail = "No Size Run"
        and B.type is  null
        group by  A.style, A.color_code,A.size, A.ORDER_NUMBER, A.NT_Num
        ) B on A.style = B.style and A.color_code = B.color_code and A.size = B.size;
        


drop table if exists container_detail_report;
create table if not exists container_detail_report
select * from container_size_run_assigned_with_container
union 
select * from container_size_run_assigned_without_container
union
select * from container_size_run_unassigned_with_container
union
select * from container_size_run_unassigned_without_container
union
select * from container_no_size_run_assigned_with_container
union
select * from container_no_size_run_assigned_without_container
union
select * from container_no_size_run_unassigned_with_container
union
select * from container_no_size_run_unassigned_without_container;



Alter table container_detail_report add column image_lookup varchar(65);
update container_detail_report A left join (select  STYLE, COLOR_CODE,  SUBSTRING_INDEX(SUBSTRING_INDEX(IMAGE_FILE, '\\', -1),".",1) as Image_lookup 
from style_master where IMAGE_FILE is not null group by  STYLE, COLOR_CODE) B using(style, color_code)
Set A.image_lookup = B.Image_lookup;


update container_detail_report set Unassigned_Orders_Qty = 0 where Unassigned_Orders_Qty is null;
update container_detail_report set Unassigned_Orders_Packs = 0 where Unassigned_Orders_Packs is null;



-- ----------------------------------------------------------------------------------------
-- PO MAPPING -------------------------------------------------------------------------
-- ----------------------------------------------------------------------------------------

drop table if exists container_po_mapping;
create table if not exists container_po_mapping
select 
Type, Size_Run, VENDOR, order_number, date, order_date, cancel_date, Nt_Num, STYLE, COLOR_CODE, color, 
SZ_RUN, RUN_CD, CLASS_CD, Size_Breakdown, Pack_Breakdown, Size_Run_Detail, PREPACK_QTY, 
"" as NUMBER, Size_Run_Detail as Size,PREPACK_QTY as Size_Pack_Qty, 
Container, "" as UPC, Image, PRICE_BASE, FRT_CUS, HNDL_FEE, PROD_DUTY, AVG_COST, sum(QTY) as QTY, Total_Pack_Qty, Unit_Packs, sum(size_Run_Qty) as size_Run_Qty, no_size_Run_Qty,
Assigned_Order_Number, customer_name, SALE_ORDER_DATE, SHIP_DATE, 
case when Assigned_Order_Number is not null then "Make Up" else "Stock" end as status,
avg(case when Assigned_Order_Number is not null then ORDER_QTY else null end) as ORDER_QTY, 
avg(case when Assigned_Order_Number is not null then Order_Prepack else null end) as Order_Prepack, 
avg(case when Assigned_Order_Number is not null then CASE_PACKS else null end) as CASE_PACKS
from container_purchase_order_planning
where Size_Run = "Size Run"
group by order_number, STYLE, color, Nt_Num;





insert into container_po_mapping
 select Type, Size_Run, VENDOR, order_number, date, order_date, cancel_date, Nt_Num, STYLE, COLOR_CODE, color, 
SZ_RUN, RUN_CD, CLASS_CD, Size_Breakdown, Pack_Breakdown, Size_Run_Detail, 0 as  PREPACK_QTY, 
"" as NUMBER, Size,PREPACK_QTY as Size_Pack_Qty, 
Container, "" as UPC, Image, PRICE_BASE, FRT_CUS, HNDL_FEE, PROD_DUTY, AVG_COST,  QTY, Total_Pack_Qty, QTY as  Unit_Packs, size_Run_Qty, no_size_Run_Qty,
Assigned_Order_Number, customer_name, SALE_ORDER_DATE, SHIP_DATE, 
case when Assigned_Order_Number is not null then "Make Up" else "Stock"  end as status,
case when Assigned_Order_Number is not null then ORDER_QTY else null end as ORDER_QTY, 
case when Assigned_Order_Number is not null then Order_Prepack else null end as Order_Prepack,
case when Assigned_Order_Number is not null then CASE_PACKS else null end as CASE_PACKS
from container_purchase_order_planning
where Size_Run != "Size Run";


-- -----------------------------------------------------------------------------------------------
-- NOT USING RIGT NOW ONLY FOR PBI CONNECTIONG----------------------------------------------------
-- -----------------------------------------------------------------------------------------------

drop table if exists container_setup_inventory;
create table if not exists container_setup_inventory
select * , 
ifnull(lag(Ending_Inventory,1) over(partition by style, color_code, size order by date, Stock, order_number),0) as Starting_Inventory from
 (select *, 
 sum(qty) over (partition by style, color_code, size order by ranking) as Ending_Inventory 
from
(select *,  row_number() over(partition by style, color_code, size order by date, Stock, order_number) as ranking
from
(select * from container_inventory_setup 
-- union
-- select * from container_po_setup
) A) A) A;

-- select * from container_inventory_setup ;
-- select * from container_po_setup;


drop table if exists container_setup_sales;
create table if not exists container_setup_sales
select *, ifnull(lag(Ending_Sales,1) over(partition by style, color_code, size order by ranking),0) as Starting_Sales from
(select *, sum(qty) over (partition by style, color_code, size order by ranking) as Ending_Sales from
(select *, 
row_number() over(partition by style, color_code, size order by Size_Run_Detail desc, date, order_number) as ranking from  container_so_setup
) A order by Ending_Sales) A;


create index unique_row on container_setup_sales(style, color_code, size, Starting_Sales);
create index unique_row on container_setup_inventory(style, color_code, size, Ending_Inventory);
create index unique_row_1 on container_setup_inventory(style, color_code, size, Starting_Inventory, Ending_Inventory);
create index ranking on container_setup_sales(style, color_code, size, ranking);
create index ranking on container_setup_inventory(style, color_code, size, ranking);


set @max_rank:= (select max(ranking) from container_setup_inventory);
drop table if exists number_setup;
create table if not exists number_setup(
id int);

insert into number_setup values
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10),
(11), (12), (13), (14), (15), (16), (17), (18), (19), (20),
(21), (22), (23), (24), (25), (26), (27), (28), (29), (30),
(31), (32), (33), (34), (35), (36), (37), (38), (39), (40),
(41), (42), (43), (44), (45), (46), (47), (48), (49), (50),
(51), (52), (53), (54), (55), (56), (57), (58), (59), (60),
(61), (62), (63), (64), (65), (66), (67), (68), (69), (70),
(71), (72), (73), (74), (75), (76), (77), (78), (79), (80),
(81), (82), (83), (84), (85), (86), (87), (88), (89), (90),
(91), (92), (93), (94), (95), (96), (97), (98), (99), (100);

delete from number_setup where id > @max_rank;



drop table if exists container_staging;
create table if not exists container_staging
select  
A.style, A.color_code, A.size, A.ranking, ifnull(B.ranking, C.Ranking) AS starting_rank, 
ifnull(ifnull(E.ranking, D.ranking),ifnull(B.ranking, C.Ranking)) as Ending_Rank
from 
container_setup_sales A 
left join container_setup_inventory B on A.style = B.style and A.color = B.color and A.size = B.size and A.Starting_Sales >=  B.Starting_Inventory and A.Ending_Sales <= B.Ending_Inventory
left join container_setup_inventory C on A.style = C.style and A.color = C.color and A.size = C.size and A.Starting_Sales >=  C.Starting_Inventory and A.Starting_Sales <  C.Ending_Inventory and A.Ending_Sales > C.Ending_Inventory
left join container_setup_inventory D on A.style = D.style and A.color = D.color and A.size = D.size and A.Starting_Sales < D.Starting_Inventory and  A.Ending_Sales  >  D.Ending_Inventory 
left join container_setup_inventory E on A.style = E.style and A.color = E.color and A.size = E.size and A.Starting_Sales < E.Starting_Inventory and  A.Ending_Sales  >  E.Starting_Inventory  and  A.Ending_Sales  <=  E.Ending_Inventory 
where A.size is not null

-- and A.style = @style and A.color_code = @color_code and A.size = @size
group by A.style, A.color_code, A.size, A.ranking
order by A.ranking;

drop table if exists container_staging_setup;
create table if not exists container_staging_setup (primary key(style, color_code, size, ranking, id))
Select *, case when starting_rank is not null then id else 1000 end as Real_ID from
(select A.style, A.color_code, A.size, A.ranking,A.starting_rank, A.Ending_Rank, B.* from
container_staging A
cross join 
number_setup B) A
where (id >= starting_rank and id <= ending_rank) or (starting_rank is null and id = 1);




create index sales_setup on container_staging_setup(style, color_code, size, ranking);
create index inventory_setup on container_staging_setup(style, color_code, size, Real_ID);


drop table if exists container_report;
create table if not exists container_report(primary key(style, color_code, size,order_id, inventory_id))
select A.style, A.color_code, B.color, A.size, A.ranking as Order_ID, A.real_id as Inventory_ID,
B.Customer, B.Order_Number, B.Size_Run_Detail, B.date as sell_date, B.order_date, B.cancel_date, 
B.RUN_CODE, B.CLASS_CODE, B.PREPACK_QTY, B.NUMBER, 
B.upc, B.image, SUBSTRING_INDEX(SUBSTRING_INDEX(B.image, "\\", -1),'.',1) as Image_lookup ,
 B.UNIT_PRICE,
B.PRICE_BASE, B.FRT_CUS	, B.HNDL_FEE, B.PROD_DUTY, B.AVG_COST, B.qty as Sales_Qty, B.Starting_Sales, B.Ending_Sales, 
C.Stock as Vendor, C.date as Received_date, C.order_date as placed_date, C.container, C.PRICE_BASE as Cost, C.QTY as Iventory_Qty, 
C.Starting_Inventory,C.Ending_Inventory,
Case when B.Starting_Sales >= C.Starting_Inventory and  B.Ending_Sales <= C.Ending_Inventory then B.qty
	 when B.Starting_Sales >= C.Starting_Inventory and  B.Ending_Sales > C.Ending_Inventory then C.Ending_Inventory - B.Starting_Sales
	 when B.Starting_Sales <= C.Starting_Inventory and  B.Ending_Sales >= C.Ending_Inventory then C.QTY
     when B.Starting_Sales <= C.Starting_Inventory and  B.Ending_Sales < C.Ending_Inventory then B.Ending_Sales - C.Starting_Inventory
end as Fulfillable_Qty
from container_staging_setup A 
left join container_setup_sales B on A.Style = B.style and A.color_code = B.color_code and A.size = B.size and A.ranking = B.ranking
left join container_setup_inventory C on A.Style = C.style and A.color_code = C.color_code and A.size = C.size and A.Real_ID = C.ranking
-- where B.style = '25025C' and B.color_code = 'blk'
order by Order_ID, NUMBER;




