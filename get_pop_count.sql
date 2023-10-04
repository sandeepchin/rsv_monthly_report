

-- Function to get the population count given a birth date range

CREATE OR REPLACE FUNCTION prd_dmowner.get_pop_count(
	dob_start VARCHAR,
	dob_end VARCHAR
	)
	RETURNS numeric AS $$
    DECLARE
	pop_count numeric;
	BEGIN
		select count(*) into pop_count
			from prd_dmowner.client_demographic c 
			where
			c.birth_date >= to_date(dob_start,'YYYY-MM-DD')
			and c.birth_date <= to_date(dob_end,'YYYY-MM-DD');
		return pop_count;
	END;
$$ language plpgsql;