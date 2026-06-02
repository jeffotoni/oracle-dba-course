BEGIN
  ORDS.ENABLE_SCHEMA(
    p_enabled             => TRUE,
    p_schema              => 'MONITOR_APP',
    p_url_mapping_type    => 'BASE_PATH',
    p_url_mapping_pattern => 'monitor_app',
    p_auto_rest_auth      => FALSE
  );

  ORDS.DEFINE_MODULE(
    p_module_name    => 'monitor',
    p_base_path      => '/monitor/',
    p_items_per_page => 25,
    p_status         => 'PUBLISHED'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'health'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'health',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT 'ok' AS status,
             SYSTIMESTAMP AS checked_at
      FROM dual
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/instance'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/instance',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT instance_name,
             status,
             database_status
      FROM v$instance
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/database'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/database',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT name,
             open_mode,
             log_mode
      FROM v$database
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/container'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/container',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container,
             USER AS current_user
      FROM dual
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sessions'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sessions',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT username,
             status,
             COUNT(*) AS total_sessions
      FROM v$session
      WHERE username IS NOT NULL
      GROUP BY username, status
      ORDER BY username, status
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/waits'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/waits',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT event,
             total_waits,
             time_waited
      FROM v$system_event
      WHERE wait_class <> 'Idle'
      ORDER BY time_waited DESC
      FETCH FIRST 10 ROWS ONLY
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sql'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/sql',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT sql_id,
 	 		 sql_fulltext,
             executions,
             elapsed_time,
             cpu_time,
             buffer_gets
      FROM v$sqlarea
      ORDER BY elapsed_time DESC
      FETCH FIRST 10 ROWS ONLY
    ]'
  );

  ORDS.DEFINE_TEMPLATE(
    p_module_name => 'monitor',
    p_pattern     => 'stats/tablespaces'
  );

  ORDS.DEFINE_HANDLER(
    p_module_name => 'monitor',
    p_pattern     => 'stats/tablespaces',
    p_method      => 'GET',
    p_source_type => ORDS.source_type_query,
    p_source      => q'[
      SELECT tablespace_name,
             used_percent,
             tablespace_size,
             used_space
      FROM dba_tablespace_usage_metrics
      ORDER BY used_percent DESC
    ]'
  );

  COMMIT;
END;