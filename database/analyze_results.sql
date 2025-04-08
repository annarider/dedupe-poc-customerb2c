select 
dedupe.cluster_id
,dedupe.confidence_score
,dedupe.first_name
,dedupe.last_name
,dedupe.member_id
,dedupe.date_of_birth
,dedupe.addstreet
,dedupe.addcity
,dedupe.addstate
,dedupe.addpostal_code
,dedupe.addcountry
,dedupe.source_email
,dedupe.source_phone
from semarchy_customer_b2c_amer.usr_mi_person_clustered_20250408 dedupe
order by cluster_id desc, confidence_score desc
;

select
*
from semarchy_customer_b2c_amer.usr_mi_person_clustered_20250408 dedupe 
where cluster_id = 143
;

select
count(dedupe.cluster_id ), dedupe.cluster_id 
from semarchy_customer_b2c_amer.usr_mi_person_clustered_20250408 dedupe 
group by cluster_id
order by count(cluster_id)
;

select
count(dedupe.cluster_id ), dedupe.cluster_id, dedupe.confidence_score 
from semarchy_customer_b2c_amer.usr_mi_person_clustered_20250408 dedupe 
group by cluster_id, dedupe.confidence_score 
order by count(cluster_id)
;
