/* Author: Sandeep Chintabathina */
-- Function to get rsv vaccination count between two date ranges


CREATE OR REPLACE FUNCTION prd_dmowner.get_rsv_count(
		dob_start VARCHAR,
		dob_end VARCHAR,
		vax_start VARCHAR,
		vax_end VARCHAR
	)
	RETURNS numeric as
	$$
	DECLARE
	vax_count numeric;
	BEGIN
		select count(*) into vax_count from (
		select c.client_id
				from 
					prd_dmowner.client_demographic c join prd_dmowner.immun_fact imm
					on c.client_id = imm.client_id
					join prd_dmowner.vaccine v
					on v.vaccine_id = imm.vaccine_id
					left join prd_dmowner.address a  --Not all clients have addresses so client table left join address
					on c.address_id = a.address_id
				where
					--imm.vaccine_group = 48  (This group includes cvx 93, report only wants 300s)
					v.cvx_code in ('93','303','304','305','306','307')
					and c.birth_date >= to_date(dob_start,'YYYY-MM-DD')
					and c.birth_date <= to_date(dob_end,'YYYY-MM-DD')
					and imm.vaccination_date >= to_date(vax_start,'YYYY-MM-DD')
					and imm.vaccination_date <= to_date(vax_end,'YYYY-MM-DD')
					and UPPER(a.state_code)='HI' --Ensuring only jurisdiction doses
			group by c.client_id
		) sub;
			return vax_count;
	END;
	$$ 
language plpgsql;
			
--trial run

--select prd_dmowner.get_rsv_count('2022-01-31','2023-09-30','2022-01-31','2023-09-30');

-- can also call this way but slower
--select * from prd_dmowner.get_rsv_count('2022-01-31','2023-09-30','2022-01-31','2023-09-30');

