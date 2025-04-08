select 'truncate table semarchy_customer_b2c_amer.' || tablename || ';'
from pg_catalog.pg_tables
where schemaname = 'semarchy_customer_b2c_amer' /* set this to your data location schema */
  and tablename not like 'dl_%'                  /* do not truncate these system tables   */
  and tablename not like 'ext_%'                 /* do not truncate these system tables   */
  and tablename like '%'                         /* add filters as needed for entities    */
  and tablename not like 'wf_%'                         
order by substr(tablename,3), tablename
;

truncate table semarchy_customer_b2c_amer.ae_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.du_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.ga_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.gd_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.ge_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.gf_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.gh_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.gi_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.gp_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.gx_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.md_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.mh_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.mi_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.mx_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.sa_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.sd_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.se_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.sf_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.um_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.xg_comm_chan_pref;
truncate table semarchy_customer_b2c_amer.ae_nickname;
truncate table semarchy_customer_b2c_amer.gd_nickname;
truncate table semarchy_customer_b2c_amer.gx_nickname;
truncate table semarchy_customer_b2c_amer.sa_nickname;
truncate table semarchy_customer_b2c_amer.ae_person;
truncate table semarchy_customer_b2c_amer.du_person;
truncate table semarchy_customer_b2c_amer.ga_person;
truncate table semarchy_customer_b2c_amer.gd_person;
truncate table semarchy_customer_b2c_amer.ge_person;
truncate table semarchy_customer_b2c_amer.gf_person;
truncate table semarchy_customer_b2c_amer.gh_person;
truncate table semarchy_customer_b2c_amer.gi_person;
truncate table semarchy_customer_b2c_amer.gp_person;
truncate table semarchy_customer_b2c_amer.gx_person;
truncate table semarchy_customer_b2c_amer.md_person;
truncate table semarchy_customer_b2c_amer.mh_person;
truncate table semarchy_customer_b2c_amer.mi_person;
truncate table semarchy_customer_b2c_amer.mx_person;
truncate table semarchy_customer_b2c_amer.sa_person;
truncate table semarchy_customer_b2c_amer.sd_person;
truncate table semarchy_customer_b2c_amer.se_person;
truncate table semarchy_customer_b2c_amer.sf_person;
truncate table semarchy_customer_b2c_amer.um_person;
truncate table semarchy_customer_b2c_amer.xg_person;
truncate table semarchy_customer_b2c_amer.ae_person_product;
truncate table semarchy_customer_b2c_amer.gd_person_product;
truncate table semarchy_customer_b2c_amer.gx_person_product;
truncate table semarchy_customer_b2c_amer.sa_person_product;
truncate table semarchy_customer_b2c_amer.ae_product;
truncate table semarchy_customer_b2c_amer.gd_product;
truncate table semarchy_customer_b2c_amer.gx_product;
truncate table semarchy_customer_b2c_amer.sa_product;