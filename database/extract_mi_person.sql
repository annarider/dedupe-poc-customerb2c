select
	b_pubid,
	b_sourceid,
	b_classname,
	b_batchid,
	b_credate,
	b_upddate,
	b_creator,
	b_updator,
	b_pendingactions,
	b_matchgrp,
	b_oldmatchgrp,
	b_xgrp,
	b_confirmationstatus,
	b_confscore,
	b_confscoretype,
	b_hassuggmerge,
	b_suggmergeid,
	b_suggmergeconfscore,
	b_suggmergeconfscoretype,
	b_suggmergemasterscount,
	id,
	b_oldsdpk,
	b_confirmedsdpk,
	first_name,
	last_name,
	phonetic_first_name,
	phonetic_last_name,
	normalized_first_name,
	normalized_last_name,
	nickname,
	member_id,
	date_of_birth,
	normalized_street,
	normalized_city,
	normalized_state,
	source_email,
	cleansed_email,
	valid_email_domain,
	source_phone,
	standardized_phone,
	phone_geocoding_data,
	value_status,
	person_type,
	addstreet,
	addcity,
	addstate,
	addpostal_code,
	addcountry,
	mdm_id,
	effective_update_date,
	guess_gender
from
	semarchy_customer_b2c_amer.mi_person;

select *
from semarchy_customer_b2c_amer.mi_person mi
where mi.standardized_phone   is null
;

-- check for count from semarchy_customer_b2c_mdm to compare
-- 337
select count(*)
from semarchy_customer_b2c_mdm.mi_person mi
;

-- check for count from semarchy_customer_b2c_amer to compare
-- 245
select count(*)
from semarchy_customer_b2c_amer.mi_person mi
;

-- check for count from semarchy_customer_b2c_mdm to compare
select *
from semarchy_customer_b2c_mdm.mi_person mi
;