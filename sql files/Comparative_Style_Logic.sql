DROP TABLE IF EXISTS COMPARATIVE_INVENTORY_DATA;
CREATE TABLE IF NOT EXISTS COMPARATIVE_INVENTORY_DATA(PRIMARY KEY(STYLE, color_code))
SELECT A.PROD_CD AS STYLE, A.PROD_CLR AS color_code,
SUM(INVENTORY_QTY) AS INVENTORY_QTY,
SUM(AVAILABLE_QTY) AS AVAILABLE_QTY,
SUM(SALES_ORDER_QTY) AS SALES_ORDER_QTY,
SUM(SIZE_PO_QTY) AS SIZE_PO_QTY,
SUM(AVAILABLE_TO_SELL_QTY) AS AVAILABLE_TO_SELL_QTY,
SUM(CASE WHEN INVENTORY_QTY<0 THEN 0 ELSE INVENTORY_QTY END) AS ADJUSTED_INVENTORY_QTY,
SUM(CASE WHEN INVENTORY_QTY <0 THEN AVAILABLE_QTY - INVENTORY_QTY ELSE AVAILABLE_QTY END) AS ADJUSTED_AVAILABLE_QTY,
SUM(CASE WHEN INVENTORY_QTY<0 THEN 0 ELSE GREATEST(INVENTORY_QTY-SALES_ORDER_QTY,0) END) AS ADJUSTED_IN_STOCK_QTY,
SUM(CASE 
	when SALES_ORDER_QTY = 0 then 0 
	WHEN GREATEST(INVENTORY_QTY,0) +  SIZE_PO_QTY  - SALES_ORDER_QTY >0 THEN 0 
	ELSE SALES_ORDER_QTY - (GREATEST(INVENTORY_QTY,0) +  SIZE_PO_QTY) END) AS UNFULFILLABLE_SALES,
SUM(case when AVAILABLE_QTY <=0 then
		CASE 
			WHEN SIZE_PO_QTY <=0 THEN 0
			WHEN SIZE_PO_QTY < (SALES_ORDER_QTY - GREATEST(INVENTORY_QTY,0)) THEN 
				case when SIZE_PO_QTY - (SALES_ORDER_QTY - GREATEST(INVENTORY_QTY,0)) <0 then 0 
                else SIZE_PO_QTY - (SALES_ORDER_QTY - GREATEST(INVENTORY_QTY,0)) 
                end 
            WHEN INVENTORY_QTY < 0 THEN GREATEST(SIZE_PO_QTY - SALES_ORDER_QTY,0)
			ELSE SIZE_PO_QTY + AVAILABLE_QTY 
        END 
	else
    case when SIZE_PO_QTY <=0 THEN 0
    else SIZE_PO_QTY end end) AS ADJUSTED_SIZE_PO_QTY,
SUM(CASE WHEN INVENTORY_QTY <0 THEN AVAILABLE_TO_SELL_QTY - INVENTORY_QTY 
		- case when SIZE_PO_QTY < 0 then SIZE_PO_QTY else 0 end
 ELSE AVAILABLE_TO_SELL_QTY - case when SIZE_PO_QTY < 0 then SIZE_PO_QTY else 0 end END) AS ADJUSTED_AVAILABLE_TO_SELL_QTY
FROM INVENTORY_DATA A
GROUP BY A.PROD_CD, A.PROD_CLR;



DROP TABLE IF EXISTS COMPARATIVE_O_STYLE_DATA;
CREATE TABLE IF NOT EXISTS COMPARATIVE_O_STYLE_DATA(PRIMARY KEY(STYLE, COLOR))
select "O-Style" as Type, O_Style as style,  
A.style AS style_ref, 
A.style_1 AS style_ref_1, 
A.style_2 AS style_ref_2, 
A.style_3 as style_ref_3,
A.Color, 
A.color_code, 
CLASS, INVENTORY_SIZE, EXPANDED_UPC, IMAGE_FILE , b.inv_sz, b.Size_Breakdown, b.Pack_Breakdown ,B.Size_Run,
-- ifnull(C.INVENTORY_QTY,0) as INVENTORY_QTY, 
-- ifnull(C.AVAILABLE_QTY, 0) as AVAILABLE_QTY, 
ifnull(C.SALES_ORDER_QTY, 0) as SALES_ORDER_QTY, 
-- ifnull(C.SIZE_PO_QTY, 0) as SIZE_PO_QTY, 
-- ifnull(C.AVAILABLE_TO_SELL_QTY, 0) as AVAILABLE_TO_SELL_QTY,
-- ifnull(C.ADJUSTED_INVENTORY_QTY, 0) as ADJUSTED_INVENTORY_QTY,
-- ifnull(C.ADJUSTED_AVAILABLE_QTY, 0) as ADJUSTED_AVAILABLE_QTY,
ifnull(C.ADJUSTED_IN_STOCK_QTY, 0) as ADJUSTED_IN_STOCK_QTY,
ifnull(C.UNFULFILLABLE_SALES, 0) as UNFULFILLABLE_SALES,
ifnull(C.ADJUSTED_SIZE_PO_QTY, 0) as ADJUSTED_SIZE_PO_QTY,
ifnull(C.ADJUSTED_AVAILABLE_TO_SELL_QTY, 0) as ADJUSTED_AVAILABLE_TO_SELL_QTY
from
(select A.style as O_Style,B.style, C.style as style_1, d.style as style_2, e.style as style_3,
ifnull(a.color,"") as color,A.color_code,  A.CLASS, A.INVENTORY_SIZE,  EXPANDED_UPC, IMAGE_FILE  from
(select style, right(style,length(style)-2) as style_ref, mid(style,3,length(style)-3) as style_ref_1, color, color_code, CLASS, INVENTORY_SIZE, EXPANDED_UPC, IMAGE_FILE from style_master where style like 'O-%' group by style, color) A 
left join (select distinct style, color  from style_master) B on A.style_ref = B.style and a.color = b.color
left join (select distinct left(style,length(style)-1) as style, color  from style_master) C on A.style_ref = c.style and a.color = c.color
left join (select distinct style, color  from style_master) D on A.style_ref_1 = d.style and a.color = d.color
left join (select distinct left(style,length(style)-1) as style, color  from style_master) E on A.style_ref_1 = e.style and a.color = e.color
) A
left join case_breakdown B on trim(A.CLASS) = trim(B.class_cd)  and a.INVENTORY_SIZE = b.inv_sz
LEFT JOIN  COMPARATIVE_INVENTORY_DATA C ON a.O_Style = c.STYLE and a.color_code = c.color_code;



DROP TABLE IF EXISTS COMPARATIVE_STYLE_DATA;
CREATE TABLE IF NOT EXISTS COMPARATIVE_STYLE_DATA(PRIMARY KEY(STYLE, COLOR))
select "Regular",style, color,color_code, CLASS, INVENTORY_SIZE, EXPANDED_UPC, IMAGE_FILE , b.inv_sz, b.Size_Breakdown, b.Pack_Breakdown ,B.Size_Run,
-- ifnull(C.INVENTORY_QTY,0) as INVENTORY_QTY, 
-- ifnull(C.AVAILABLE_QTY, 0) as AVAILABLE_QTY, 
ifnull(C.SALES_ORDER_QTY, 0) as SALES_ORDER_QTY, 
-- ifnull(C.SIZE_PO_QTY, 0) as SIZE_PO_QTY, 
-- ifnull(C.AVAILABLE_TO_SELL_QTY, 0) as AVAILABLE_TO_SELL_QTY,
-- ifnull(C.ADJUSTED_INVENTORY_QTY, 0) as ADJUSTED_INVENTORY_QTY,
-- ifnull(C.ADJUSTED_AVAILABLE_QTY, 0) as ADJUSTED_AVAILABLE_QTY,
ifnull(C.ADJUSTED_IN_STOCK_QTY, 0) as ADJUSTED_IN_STOCK_QTY,
ifnull(C.UNFULFILLABLE_SALES, 0) as UNFULFILLABLE_SALES,
ifnull(C.ADJUSTED_SIZE_PO_QTY, 0) as ADJUSTED_SIZE_PO_QTY,
ifnull(C.ADJUSTED_AVAILABLE_TO_SELL_QTY, 0) as ADJUSTED_AVAILABLE_TO_SELL_QTY
from
(select A.style as O_Style, A.style,  ifnull(A.color,"") as color,A.color_code,  A.CLASS, A.INVENTORY_SIZE,  EXPANDED_UPC, IMAGE_FILE  from
(select style, right(style,length(style)-2) as style_ref, color,color_code,  CLASS, INVENTORY_SIZE,  EXPANDED_UPC, IMAGE_FILE   from style_master where active = "Y" group by style, color) A 
left join (select distinct style , color from style_master) B on A.style_ref = B.style and a.color = b.color) A
left join case_breakdown B on trim(A.CLASS) = trim(B.class_cd)  and a.INVENTORY_SIZE = b.inv_sz
LEFT JOIN  COMPARATIVE_INVENTORY_DATA C USING(STYLE, color_code);


Alter table COMPARATIVE_STYLE_DATA 
add column style_ref_1 varchar(65);

update COMPARATIVE_STYLE_DATA a
set 
style_ref_1 =  left(A.style,length(A.style)-1);

create index style_ref_1 on COMPARATIVE_STYLE_DATA(style_ref_1);


create index style_ref on COMPARATIVE_O_STYLE_DATA(style_ref);
create index style_ref_1 on COMPARATIVE_O_STYLE_DATA(style_ref_1);
create index style_ref_2 on COMPARATIVE_O_STYLE_DATA(style_ref_2);
create index style_ref_3 on COMPARATIVE_O_STYLE_DATA(style_ref_3);



DROP TABLE IF EXISTS COMPARATIVE_STYLE_REPORT;
CREATE TABLE IF NOT EXISTS COMPARATIVE_STYLE_REPORT(PRIMARY KEY(Regular_Style, Regular_Color))
select 
A.style as Regular_Style,
a.COLOR as Regular_Color, 
A.color_code as Regular_Color_Code,
A.CLASS as Regular_Class,
A.INVENTORY_SIZE as Regular_Inv_SIZE,
A.Size_Run as Regular_Size_Run,
A.Size_Breakdown as Regular_Size_Breakdown,
A.Pack_Breakdown as Regular_Pack_Breakdown,
A.IMAGE_FILE as Regular_Image,
A.EXPANDED_UPC as Regular_Upc,
A.ADJUSTED_IN_STOCK_QTY as Regular_INVENTORY_QTY,
A.UNFULFILLABLE_SALES as Regular_UNFULFILLABLE_SALES,
A.SALES_ORDER_QTY as Regular_SALES_ORDER_QTY,
A.ADJUSTED_SIZE_PO_QTY as Regular_SIZE_PO_QTY,
A.ADJUSTED_AVAILABLE_TO_SELL_QTY as Regular_AVAILABLE_TO_SELL_QTY,
ifnull(ifnull(ifnull(ifnull(B.style, c.style),d.style),e.style),f.style) as O_Style,
ifnull(ifnull(ifnull(ifnull(b.COLOR, C.color),d.color),e.color), f.color) as O_Color,
ifnull(ifnull(ifnull(ifnull(b.color_code, C.color_code),d.color_code),e.color_code), f.color_code) as O_Color_Code,
ifnull(ifnull(ifnull(ifnull(b.class, C.class),d.class),e.class), f.class) as O_Class,
ifnull(ifnull(ifnull(ifnull(b.INVENTORY_SIZE, C.INVENTORY_SIZE),d.INVENTORY_SIZE),e.INVENTORY_SIZE), f.INVENTORY_SIZE) as O_Inv_SIZE,
ifnull(ifnull(ifnull(ifnull(b.Size_Run, C.Size_Run),d.Size_Run),e.Size_Run), f.Size_Run) as O_Size_Run,
ifnull(ifnull(ifnull(ifnull(b.Size_Breakdown, C.Size_Breakdown),d.Size_Breakdown),e.Size_Breakdown), f.Size_Breakdown) as O_Size_Breakdown,
ifnull(ifnull(ifnull(ifnull(b.Pack_Breakdown, C.Pack_Breakdown),d.Pack_Breakdown),e.Pack_Breakdown), f.Pack_Breakdown) as O_Pack_Breakdown,
ifnull(ifnull(ifnull(ifnull(b.IMAGE_FILE, C.IMAGE_FILE),d.IMAGE_FILE),e.IMAGE_FILE), f.IMAGE_FILE) as O_Image,
ifnull(ifnull(ifnull(ifnull(b.EXPANDED_UPC, C.EXPANDED_UPC),d.EXPANDED_UPC),e.EXPANDED_UPC), f.EXPANDED_UPC) as O_Upc,
ifnull(ifnull(ifnull(ifnull(b.ADJUSTED_IN_STOCK_QTY, C.ADJUSTED_IN_STOCK_QTY),d.ADJUSTED_IN_STOCK_QTY),e.ADJUSTED_IN_STOCK_QTY), f.ADJUSTED_IN_STOCK_QTY) as O_INVENTORY_QTY,
-- ifnull(B.UNFULFILLABLE_SALES, c.UNFULFILLABLE_SALES) as O_UNFULFILLABLE_SALES,
ifnull(ifnull(ifnull(ifnull(b.SALES_ORDER_QTY, C.SALES_ORDER_QTY),d.SALES_ORDER_QTY),e.SALES_ORDER_QTY), f.SALES_ORDER_QTY) as O_SALES_ORDER_QTY,
ifnull(ifnull(ifnull(ifnull(b.ADJUSTED_SIZE_PO_QTY, C.ADJUSTED_SIZE_PO_QTY),d.ADJUSTED_SIZE_PO_QTY),e.ADJUSTED_SIZE_PO_QTY), f.ADJUSTED_SIZE_PO_QTY) as O_SIZE_PO_QTY,
ifnull(ifnull(ifnull(ifnull(b.ADJUSTED_AVAILABLE_TO_SELL_QTY, C.ADJUSTED_IN_STOCK_QTY),d.ADJUSTED_AVAILABLE_TO_SELL_QTY),e.ADJUSTED_AVAILABLE_TO_SELL_QTY), f.ADJUSTED_AVAILABLE_TO_SELL_QTY) as O_AVAILABLE_TO_SELL_QTY,
row_number() over (partition by  A.style order by  a.COLOR) as STYLE_RANKING
from 
COMPARATIVE_STYLE_DATA A 
left join COMPARATIVE_O_STYLE_DATA B on A.style = B.style_ref and a.color = B.color
left join COMPARATIVE_O_STYLE_DATA C on A.style_ref_1 = c.style_ref_1 and a.color = c.color
left join COMPARATIVE_O_STYLE_DATA d on A.style = d.style_ref_2 and a.color = d.color
left join COMPARATIVE_O_STYLE_DATA e on A.style_ref_1 = e.style_ref_3 and a.color = e.color
left join COMPARATIVE_O_STYLE_DATA f  on A.style_ref_1 = f.style_ref_2 and a.color = f.color
group by Regular_Style, Regular_Color;




DROP TABLE IF EXISTS COMPARATIVE_INVENTORY_DATA_BY_SIZE;
CREATE TABLE IF NOT EXISTS COMPARATIVE_INVENTORY_DATA_BY_SIZE(PRIMARY KEY(STYLE, COLOR_CODE, SIZE))
SELECT A.PROD_CD AS STYLE, A.PROD_CLR AS COLOR_CODE, A.Size_Breakdown AS Size,
SUM(INVENTORY_QTY) AS INVENTORY_QTY,
SUM(AVAILABLE_QTY) AS AVAILABLE_QTY,
SUM(SALES_ORDER_QTY) AS SALES_ORDER_QTY,
SUM(SIZE_PO_QTY) AS SIZE_PO_QTY,
SUM(AVAILABLE_TO_SELL_QTY) AS AVAILABLE_TO_SELL_QTY,
SUM(CASE WHEN INVENTORY_QTY<0 THEN 0 ELSE INVENTORY_QTY END) AS ADJUSTED_INVENTORY_QTY,
SUM(CASE WHEN INVENTORY_QTY <0 THEN AVAILABLE_QTY - INVENTORY_QTY ELSE AVAILABLE_QTY END) AS ADJUSTED_AVAILABLE_QTY,
SUM(CASE WHEN INVENTORY_QTY<0 THEN 0 ELSE GREATEST(INVENTORY_QTY-SALES_ORDER_QTY,0) END) AS ADJUSTED_IN_STOCK_QTY,
SUM(CASE 
	when SALES_ORDER_QTY = 0 then 0 
	WHEN GREATEST(INVENTORY_QTY,0) +  SIZE_PO_QTY  - SALES_ORDER_QTY >0 THEN 0 
	ELSE SALES_ORDER_QTY - (GREATEST(INVENTORY_QTY,0) +  SIZE_PO_QTY) END) AS UNFULFILLABLE_SALES,
SUM(case when AVAILABLE_QTY <=0 then
		CASE 
			WHEN SIZE_PO_QTY <=0 THEN 0
			WHEN SIZE_PO_QTY < (SALES_ORDER_QTY - GREATEST(INVENTORY_QTY,0)) THEN 
				case when SIZE_PO_QTY - (SALES_ORDER_QTY - GREATEST(INVENTORY_QTY,0)) <0 then 0 
                else SIZE_PO_QTY - (SALES_ORDER_QTY - GREATEST(INVENTORY_QTY,0)) 
                end 
            WHEN INVENTORY_QTY < 0 THEN GREATEST(SIZE_PO_QTY - SALES_ORDER_QTY,0)
			ELSE SIZE_PO_QTY + AVAILABLE_QTY 
        END 
	else
    case when SIZE_PO_QTY <=0 THEN 0
    else SIZE_PO_QTY end end) AS ADJUSTED_SIZE_PO_QTY,
SUM(CASE WHEN INVENTORY_QTY <0 THEN AVAILABLE_TO_SELL_QTY - INVENTORY_QTY 
		- case when SIZE_PO_QTY < 0 then SIZE_PO_QTY else 0 end
 ELSE AVAILABLE_TO_SELL_QTY - case when SIZE_PO_QTY < 0 then SIZE_PO_QTY else 0 end END) AS ADJUSTED_AVAILABLE_TO_SELL_QTY
FROM INVENTORY_DATA A
GROUP BY A.PROD_CD, A.PROD_CLR, A.Size_Breakdown;



DROP TABLE IF EXISTS COMPARATIVE_O_STYLE_DATA_BY_SIZE;
CREATE TABLE IF NOT EXISTS COMPARATIVE_O_STYLE_DATA_BY_SIZE(PRIMARY KEY(STYLE, COLOR, SIZE))
select "O-Style" as Type, O_Style as style,  
A.style AS style_ref, 
A.style_1 AS style_ref_1, 
A.style_2 AS style_ref_2, 
A.style_3 as style_ref_3,
ifnull(A.SIZE,"") as Size, A.number,
 A.Color, 
 A.Color_code,
 CLASS, INVENTORY_SIZE, EXPANDED_UPC, IMAGE_FILE , b.inv_sz, b.Size_Breakdown, b.Pack_Breakdown ,B.Size_Run,
-- ifnull(C.INVENTORY_QTY,0) as INVENTORY_QTY, 
-- ifnull(C.AVAILABLE_QTY, 0) as AVAILABLE_QTY, 
ifnull(C.SALES_ORDER_QTY, 0) as SALES_ORDER_QTY, 
-- ifnull(C.SIZE_PO_QTY, 0) as SIZE_PO_QTY, 
-- ifnull(C.AVAILABLE_TO_SELL_QTY, 0) as AVAILABLE_TO_SELL_QTY,
-- ifnull(C.ADJUSTED_INVENTORY_QTY, 0) as ADJUSTED_INVENTORY_QTY,
-- ifnull(C.ADJUSTED_AVAILABLE_QTY, 0) as ADJUSTED_AVAILABLE_QTY,
ifnull(C.ADJUSTED_IN_STOCK_QTY, 0) as ADJUSTED_IN_STOCK_QTY,
ifnull(C.UNFULFILLABLE_SALES, 0) as UNFULFILLABLE_SALES,
ifnull(C.ADJUSTED_SIZE_PO_QTY, 0) as ADJUSTED_SIZE_PO_QTY,
ifnull(C.ADJUSTED_AVAILABLE_TO_SELL_QTY, 0) as ADJUSTED_AVAILABLE_TO_SELL_QTY
from
(select A.style as O_Style, B.style, C.style as style_1, d.style as style_2, e.style as style_3,
ifnull(a.color,"") as color, A.Color_code,A.Size,A.number,  A.CLASS, A.INVENTORY_SIZE,  EXPANDED_UPC, IMAGE_FILE  from
(select style, right(style,length(style)-2) as style_ref,  mid(style,3,length(style)-3) as style_ref_1, color,Color_code,Size, number, CLASS, INVENTORY_SIZE, EXPANDED_UPC, IMAGE_FILE from style_master where style like 'O-%' group by style, color, Size) A 
left join (select distinct style, color, Size  from style_master) B on A.style_ref = B.style and a.color = b.color and a.size = b.size
left join (select distinct left(style,length(style)-1) as style, color, Size  from style_master) C on A.style_ref = c.style and a.color = c.color and  a.size = c.size
left join (select distinct style, color, Size  from style_master) D on A.style_ref_1 = d.style and a.color = d.color and  a.size =d.size
left join (select distinct left(style,length(style)-1) as style, color , Size from style_master) E on A.style_ref_1 = e.style and a.color = e.color and  a.size = e.size
) A
left join case_breakdown B on trim(A.CLASS) = trim(B.class_cd)  and a.INVENTORY_SIZE = b.inv_sz
LEFT JOIN  COMPARATIVE_INVENTORY_DATA_BY_SIZE C ON a.O_Style = c.STYLE and a.COLOR_CODE = c.COLOR_CODE AND A.size= c.size;



DROP TABLE IF EXISTS COMPARATIVE_STYLE_DATA_BY_SIZE;
CREATE TABLE IF NOT EXISTS COMPARATIVE_STYLE_DATA_BY_SIZE(PRIMARY KEY(STYLE, COLOR, SIZE))
select "Regular",style, color,color_code, ifnull(SIZE,"") as SIZE,number,  CLASS, INVENTORY_SIZE, EXPANDED_UPC, IMAGE_FILE , b.inv_sz, b.Size_Breakdown, b.Pack_Breakdown ,B.Size_Run,
-- ifnull(C.INVENTORY_QTY,0) as INVENTORY_QTY, 
-- ifnull(C.AVAILABLE_QTY, 0) as AVAILABLE_QTY, 
ifnull(C.SALES_ORDER_QTY, 0) as SALES_ORDER_QTY, 
-- ifnull(C.SIZE_PO_QTY, 0) as SIZE_PO_QTY, 
-- ifnull(C.AVAILABLE_TO_SELL_QTY, 0) as AVAILABLE_TO_SELL_QTY,
-- ifnull(C.ADJUSTED_INVENTORY_QTY, 0) as ADJUSTED_INVENTORY_QTY,
-- ifnull(C.ADJUSTED_AVAILABLE_QTY, 0) as ADJUSTED_AVAILABLE_QTY,
ifnull(C.ADJUSTED_IN_STOCK_QTY, 0) as ADJUSTED_IN_STOCK_QTY,
ifnull(C.UNFULFILLABLE_SALES, 0) as UNFULFILLABLE_SALES,
ifnull(C.ADJUSTED_SIZE_PO_QTY, 0) as ADJUSTED_SIZE_PO_QTY,
ifnull(C.ADJUSTED_AVAILABLE_TO_SELL_QTY, 0) as ADJUSTED_AVAILABLE_TO_SELL_QTY
from
(select A.style as O_Style, A.style,  ifnull(A.color,"") as color,color_code, A.SIZE, A.number, A.CLASS, A.INVENTORY_SIZE,  EXPANDED_UPC, IMAGE_FILE  from
(select style, right(style,length(style)-2) as style_ref, color,color_code,SIZE, number, CLASS, INVENTORY_SIZE,  EXPANDED_UPC, IMAGE_FILE   from style_master where active = "Y" group by style, color, SIZE) A 
left join (select distinct style , color, SIZE from style_master) B on A.style_ref = B.style and a.color = b.color AND  A.SIZE = B.SIZE) A
left join case_breakdown B on A.CLASS = B.class_cd  and a.INVENTORY_SIZE = b.inv_sz
LEFT JOIN  COMPARATIVE_INVENTORY_DATA_by_size C USING(STYLE, COLOR_CODE, SIZE);


Alter table COMPARATIVE_STYLE_DATA_by_size 
add column style_ref_1 varchar(65);

update COMPARATIVE_STYLE_DATA_by_size a
set 
style_ref_1 =  left(A.style,length(A.style)-1);

create index style_ref on COMPARATIVE_STYLE_DATA_by_size(style);
create index style_ref_1 on COMPARATIVE_STYLE_DATA_by_size(style_ref_1);

create index style_ref on COMPARATIVE_O_STYLE_DATA_BY_SIZE(style_ref);
create index style_ref_1 on COMPARATIVE_O_STYLE_DATA_BY_SIZE(style_ref_1);
create index style_ref_2 on COMPARATIVE_O_STYLE_DATA_BY_SIZE(style_ref_2);
create index style_ref_3 on COMPARATIVE_O_STYLE_DATA_BY_SIZE(style_ref_3);



DROP TABLE IF EXISTS COMPARATIVE_STYLE_REPORT_BY_SIZE;
CREATE TABLE IF NOT EXISTS COMPARATIVE_STYLE_REPORT_BY_SIZE(PRIMARY KEY(Regular_Style, Regular_Color, Regular_Size))
select 
A.style as Regular_Style,
a.COLOR as Regular_Color, 
A.number as Regular_Number,
a.Size as Regular_Size, 
A.CLASS as Regular_Class,
A.INVENTORY_SIZE as Regular_Inv_SIZE,
A.Size_Run as Regular_Size_Run,
A.Size_Breakdown as Regular_Size_Breakdown,
A.Pack_Breakdown as Regular_Pack_Breakdown,
A.IMAGE_FILE as Regular_Image,
A.EXPANDED_UPC as Regular_Upc,
A.ADJUSTED_IN_STOCK_QTY as Regular_INVENTORY_QTY,
A.UNFULFILLABLE_SALES as Regular_UNFULFILLABLE_SALES,
A.SALES_ORDER_QTY as Regular_SALES_ORDER_QTY,
A.ADJUSTED_SIZE_PO_QTY as Regular_SIZE_PO_QTY,
A.ADJUSTED_AVAILABLE_TO_SELL_QTY as Regular_AVAILABLE_TO_SELL_QTY,
ifnull(ifnull(ifnull(ifnull(B.style, c.style),d.style),e.style),f.style) as O_Style,
ifnull(ifnull(ifnull(ifnull(b.COLOR, C.color),d.color),e.color), f.color) as O_Color,
ifnull(ifnull(ifnull(ifnull(b.color_code, C.color_code),d.color_code),e.color_code), f.color_code) as O_Color_Code,
ifnull(ifnull(ifnull(ifnull(b.class, C.class),d.class),e.class), f.class) as O_Class,
ifnull(ifnull(ifnull(ifnull(b.INVENTORY_SIZE, C.INVENTORY_SIZE),d.INVENTORY_SIZE),e.INVENTORY_SIZE), f.INVENTORY_SIZE) as O_Inv_SIZE,
ifnull(ifnull(ifnull(ifnull(b.Size_Run, C.Size_Run),d.Size_Run),e.Size_Run), f.Size_Run) as O_Size_Run,
ifnull(ifnull(ifnull(ifnull(b.Size_Breakdown, C.Size_Breakdown),d.Size_Breakdown),e.Size_Breakdown), f.Size_Breakdown) as O_Size_Breakdown,
ifnull(ifnull(ifnull(ifnull(b.Pack_Breakdown, C.Pack_Breakdown),d.Pack_Breakdown),e.Pack_Breakdown), f.Pack_Breakdown) as O_Pack_Breakdown,
ifnull(ifnull(ifnull(ifnull(b.IMAGE_FILE, C.IMAGE_FILE),d.IMAGE_FILE),e.IMAGE_FILE), f.IMAGE_FILE) as O_Image,
ifnull(ifnull(ifnull(ifnull(b.EXPANDED_UPC, C.EXPANDED_UPC),d.EXPANDED_UPC),e.EXPANDED_UPC), f.EXPANDED_UPC) as O_Upc,
ifnull(ifnull(ifnull(ifnull(b.ADJUSTED_IN_STOCK_QTY, C.ADJUSTED_IN_STOCK_QTY),d.ADJUSTED_IN_STOCK_QTY),e.ADJUSTED_IN_STOCK_QTY), f.ADJUSTED_IN_STOCK_QTY) as O_INVENTORY_QTY,
-- ifnull(B.UNFULFILLABLE_SALES, c.UNFULFILLABLE_SALES) as O_UNFULFILLABLE_SALES,
ifnull(ifnull(ifnull(ifnull(b.SALES_ORDER_QTY, C.SALES_ORDER_QTY),d.SALES_ORDER_QTY),e.SALES_ORDER_QTY), f.SALES_ORDER_QTY) as O_SALES_ORDER_QTY,
ifnull(ifnull(ifnull(ifnull(b.ADJUSTED_SIZE_PO_QTY, C.ADJUSTED_SIZE_PO_QTY),d.ADJUSTED_SIZE_PO_QTY),e.ADJUSTED_SIZE_PO_QTY), f.ADJUSTED_SIZE_PO_QTY) as O_SIZE_PO_QTY,
ifnull(ifnull(ifnull(ifnull(b.ADJUSTED_AVAILABLE_TO_SELL_QTY, C.ADJUSTED_IN_STOCK_QTY),d.ADJUSTED_AVAILABLE_TO_SELL_QTY),e.ADJUSTED_AVAILABLE_TO_SELL_QTY), f.ADJUSTED_AVAILABLE_TO_SELL_QTY) as O_AVAILABLE_TO_SELL_QTY,
row_number() over (partition by  A.style order by  a.COLOR, A.number) as STYLE_RANKING
from
COMPARATIVE_STYLE_DATA_by_size A 
left join COMPARATIVE_O_STYLE_DATA_BY_SIZE B on A.style = B.style_ref and a.color = B.color and A.size = B.size
left join COMPARATIVE_O_STYLE_DATA_BY_SIZE C on A.style_ref_1 = c.style_ref_1 and a.color = c.color and a.size = c.size
left join COMPARATIVE_O_STYLE_DATA_BY_SIZE d on A.style = d.style_ref_2 and a.color = d.color and a.size = d.size
left join COMPARATIVE_O_STYLE_DATA_BY_SIZE e on A.style_ref_1 = e.style_ref_3 and a.color = e.color and a.size = e.size
left join COMPARATIVE_O_STYLE_DATA_BY_SIZE f  on A.style_ref_1 = f.style_ref_2 and a.color = f.color and a.size = f.size
group by Regular_Style, Regular_Color, Regular_Size;
