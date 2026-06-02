'use strict';

/*
  Ajuste esta constante se o mapping do ORDS for diferente.

  Estrutura esperada:
  http://localhost:8181/ords/{schema_mapping}/{module_base_path}

  Exemplo:
  Schema ORDS: monitor_app
  Module base path: /monitor/
*/
const API_BASE = 'http://localhost:8181/ords/monitor_app/monitor';

const REFRESH_INTERVAL_MS = 10000;

const endpoints = {
  health: '/health',
  instance: '/stats/instance',
  database: '/stats/database',
  container: '/stats/container',
  sessions: '/stats/sessions',
  waits: '/stats/waits',
  sql: '/stats/sql',
  tablespaces: '/stats/tablespaces'
};

let refreshTimer = null;

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('api-base').textContent = API_BASE;

  document
    .getElementById('refresh-button')
    .addEventListener('click', loadDashboard);

  loadDashboard();

  refreshTimer = setInterval(loadDashboard, REFRESH_INTERVAL_MS);
});

async function loadDashboard() {
  setGlobalStatus('loading', 'Atualizando');

  const results = await Promise.allSettled([
    fetchFromOrds(endpoints.health),
    fetchFromOrds(endpoints.instance),
    fetchFromOrds(endpoints.database),
    fetchFromOrds(endpoints.container),
    fetchFromOrds(endpoints.sessions),
    fetchFromOrds(endpoints.waits),
    fetchFromOrds(endpoints.sql),
    fetchFromOrds(endpoints.tablespaces)
  ]);

  const [
    healthResult,
    instanceResult,
    databaseResult,
    containerResult,
    sessionsResult,
    waitsResult,
    sqlResult,
    tablespacesResult
  ] = results;

  updateHealthCard(healthResult);
  updateInstanceCard(instanceResult);
  updateDatabaseCard(databaseResult);
  updateContainerCard(containerResult);

  updateSessionsTable(sessionsResult);
  updateWaitsTable(waitsResult);
  updateSqlTable(sqlResult);
  updateTablespacesTable(tablespacesResult);

  updateLastUpdated();

  const hasError = results.some((result) => result.status === 'rejected');

  if (hasError) {
    setGlobalStatus('warning', 'Parcial');
  } else {
    setGlobalStatus('success', 'Online');
  }
}

async function fetchFromOrds(path) {
  const url = `${API_BASE}${path}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      Accept: 'application/json'
    },
    cache: 'no-store'
  });

  if (!response.ok) {
    throw new Error(`Erro HTTP ${response.status} ao consultar ${url}`);
  }

  return response.json();
}

function getItems(payload) {
  if (!payload) {
    return [];
  }

  if (Array.isArray(payload.items)) {
    return payload.items;
  }

  if (Array.isArray(payload)) {
    return payload;
  }

  return [payload];
}

function getFirstItem(payload) {
  const items = getItems(payload);
  return items.length > 0 ? items[0] : {};
}

function getValue(row, ...keys) {
  if (!row) {
    return null;
  }

  for (const key of keys) {
    if (Object.prototype.hasOwnProperty.call(row, key)) {
      return row[key];
    }

    const lowerKey = key.toLowerCase();
    if (Object.prototype.hasOwnProperty.call(row, lowerKey)) {
      return row[lowerKey];
    }

    const upperKey = key.toUpperCase();
    if (Object.prototype.hasOwnProperty.call(row, upperKey)) {
      return row[upperKey];
    }
  }

  return null;
}

function updateHealthCard(result) {
  const element = document.getElementById('card-health');

  if (result.status === 'rejected') {
    element.textContent = 'Erro';
    return;
  }

  const row = getFirstItem(result.value);
  const status = getValue(row, 'status', 'STATUS');

  element.textContent = status || 'OK';
}

function updateInstanceCard(result) {
  const nameElement = document.getElementById('card-instance-name');
  const statusElement = document.getElementById('card-instance-status');

  if (result.status === 'rejected') {
    nameElement.textContent = 'Erro';
    statusElement.textContent = 'Não foi possível consultar v$instance';
    return;
  }

  const row = getFirstItem(result.value);

  const instanceName = getValue(row, 'instance_name', 'INSTANCE_NAME');
  const status = getValue(row, 'status', 'STATUS');
  const databaseStatus = getValue(row, 'database_status', 'DATABASE_STATUS');

  nameElement.textContent = instanceName || '-';
  statusElement.textContent = `Status: ${status || '-'} | Database: ${databaseStatus || '-'}`;
}

function updateDatabaseCard(result) {
  const nameElement = document.getElementById('card-database-name');
  const modeElement = document.getElementById('card-database-mode');

  if (result.status === 'rejected') {
    nameElement.textContent = 'Erro';
    modeElement.textContent = 'Não foi possível consultar v$database';
    return;
  }

  const row = getFirstItem(result.value);

  const databaseName = getValue(row, 'name', 'NAME');
  const openMode = getValue(row, 'open_mode', 'OPEN_MODE');
  const logMode = getValue(row, 'log_mode', 'LOG_MODE');

  nameElement.textContent = databaseName || '-';
  modeElement.textContent = `Open mode: ${openMode || '-'} | Log mode: ${logMode || '-'}`;
}

function updateContainerCard(result) {
  const element = document.getElementById('card-container');

  if (result.status === 'rejected') {
    element.textContent = 'Erro';
    return;
  }

  const row = getFirstItem(result.value);
  const container = getValue(row, 'current_container', 'CURRENT_CONTAINER');

  element.textContent = container || '-';
}

function updateSessionsTable(result) {
  const tbody = document.getElementById('sessions-table-body');

  if (result.status === 'rejected') {
    renderErrorRow(tbody, 3, 'Erro ao consultar sessões.');
    return;
  }

  const items = getItems(result.value);

  if (items.length === 0) {
    renderEmptyRow(tbody, 3, 'Nenhuma sessão encontrada.');
    return;
  }

  tbody.innerHTML = items
    .map((row) => {
      const username = getValue(row, 'username', 'USERNAME') || '-';
      const status = getValue(row, 'status', 'STATUS') || '-';
      const total = getValue(row, 'total_sessions', 'TOTAL_SESSIONS') || 0;

      return `
        <tr>
          <td>${escapeHtml(username)}</td>
          <td>${escapeHtml(status)}</td>
          <td>${formatNumber(total)}</td>
        </tr>
      `;
    })
    .join('');
}

function updateWaitsTable(result) {
  const tbody = document.getElementById('waits-table-body');

  if (result.status === 'rejected') {
    renderErrorRow(tbody, 3, 'Erro ao consultar waits.');
    return;
  }

  const items = getItems(result.value);

  if (items.length === 0) {
    renderEmptyRow(tbody, 3, 'Nenhum wait encontrado.');
    return;
  }

  tbody.innerHTML = items
    .map((row) => {
      const event = getValue(row, 'event', 'EVENT') || '-';
      const totalWaits = getValue(row, 'total_waits', 'TOTAL_WAITS') || 0;
      const timeWaited = getValue(row, 'time_waited', 'TIME_WAITED') || 0;

      return `
        <tr>
          <td>${escapeHtml(event)}</td>
          <td>${formatNumber(totalWaits)}</td>
          <td>${formatOracleWaitTime(timeWaited)}</td>
        </tr>
      `;
    })
    .join('');
}

function updateSqlTable(result) {
  const tbody = document.getElementById('sql-table-body');

  if (result.status === 'rejected') {
    renderErrorRow(tbody, 5, 'Erro ao consultar SQLs custosos.');
    return;
  }

  const items = getItems(result.value);

  if (items.length === 0) {
    renderEmptyRow(tbody, 5, 'Nenhum SQL encontrado.');
    return;
  }

  tbody.innerHTML = items
    .map((row) => {
      const sqlId = getValue(row, 'sql_id', 'SQL_ID') || '-';
      const executions = getValue(row, 'executions', 'EXECUTIONS') || 0;
      const elapsedTime = getValue(row, 'elapsed_time', 'ELAPSED_TIME') || 0;
      const cpuTime = getValue(row, 'cpu_time', 'CPU_TIME') || 0;
      const bufferGets = getValue(row, 'buffer_gets', 'BUFFER_GETS') || 0;

      /*
        Campo novo vindo do endpoint ORDS:
        sql_fulltext

        Deixei fallback para sql_text caso algum endpoint antigo
        ainda retorne apenas a versão resumida.
      */
      const sqlFullText =
        getValue(row, 'sql_fulltext', 'SQL_FULLTEXT') ||
        getValue(row, 'sql_text', 'SQL_TEXT') ||
        'SQL_FULLTEXT não retornado pelo endpoint.';

      const encodedSql = encodeURIComponent(String(sqlFullText));
      // console.log(encodedSql)
      return `
        <tr>
          <td>
            <code
              class="sql-id-hover"
              tabindex="0"
              data-sql-fulltext="${encodedSql}"
              aria-label="Passe o mouse para visualizar o SQL completo"
            >${escapeHtml(sqlId)}</code>
          </td>
          <td>${formatNumber(executions)}</td>
          <td>${formatMicroseconds(elapsedTime)}</td>
          <td>${formatMicroseconds(cpuTime)}</td>
          <td>${formatNumber(bufferGets)}</td>
        </tr>
      `;
    })
    .join('');

  bindSqlTooltips();
}

function updateTablespacesTable(result) {
  const tbody = document.getElementById('tablespaces-table-body');

  if (result.status === 'rejected') {
    renderErrorRow(tbody, 3, 'Erro ao consultar tablespaces. Verifique privilégios.');
    return;
  }

  const items = getItems(result.value);

  if (items.length === 0) {
    renderEmptyRow(tbody, 3, 'Nenhum tablespace encontrado.');
    return;
  }

  tbody.innerHTML = items
    .map((row) => {
      const tablespaceName = getValue(row, 'tablespace_name', 'TABLESPACE_NAME') || '-';
      const usedPercentRaw = getValue(row, 'used_percent', 'USED_PERCENT') || 0;
      const usedPercent = Number(usedPercentRaw);

      return `
        <tr>
          <td>${escapeHtml(tablespaceName)}</td>
          <td>${formatPercent(usedPercent)}</td>
          <td>
            <div class="progress">
              <div class="progress-bar" style="width: ${clamp(usedPercent, 0, 100)}%"></div>
            </div>
          </td>
        </tr>
      `;
    })
    .join('');
}

function renderErrorRow(tbody, colspan, message) {
  tbody.innerHTML = `
    <tr>
      <td colspan="${colspan}" class="table-message table-error">${escapeHtml(message)}</td>
    </tr>
  `;
}

function renderEmptyRow(tbody, colspan, message) {
  tbody.innerHTML = `
    <tr>
      <td colspan="${colspan}" class="table-message">${escapeHtml(message)}</td>
    </tr>
  `;
}

function setGlobalStatus(type, text) {
  const element = document.getElementById('status-pill');

  element.className = 'status-pill';

  if (type === 'success') {
    element.classList.add('status-success');
  } else if (type === 'warning') {
    element.classList.add('status-warning');
  } else if (type === 'error') {
    element.classList.add('status-error');
  } else {
    element.classList.add('status-loading');
  }

  element.textContent = text;
}

function updateLastUpdated() {
  const element = document.getElementById('last-updated');

  const now = new Date();

  element.textContent = now.toLocaleString('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'medium'
  });
}

function formatNumber(value) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return '-';
  }

  return number.toLocaleString('pt-BR');
}

/*
  Em algumas views Oracle, elapsed_time e cpu_time em v$sqlarea
  são retornados em microssegundos.
*/
function formatMicroseconds(value) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return '-';
  }

  const seconds = number / 1_000_000;

  return `${seconds.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}s`;
}

/*
  Em v$system_event, time_waited costuma ser medido em centésimos de segundo.
  Por isso, dividimos por 100 para exibir uma leitura mais amigável.
*/
function formatOracleWaitTime(value) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return '-';
  }

  const seconds = number / 100;

  return `${seconds.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}s`;
}

function formatPercent(value) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return '-';
  }

  return `${number.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}%`;
}

function clamp(value, min, max) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return min;
  }

  return Math.min(Math.max(number, min), max);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

let sqlTooltipElement = null;

function bindSqlTooltips() {
  const elements = document.querySelectorAll('.sql-id-hover');

  elements.forEach((element) => {
    element.addEventListener('mouseenter', showSqlTooltip);
    element.addEventListener('mousemove', moveSqlTooltip);
    element.addEventListener('mouseleave', hideSqlTooltip);

    element.addEventListener('focus', showSqlTooltipByFocus);
    element.addEventListener('blur', hideSqlTooltip);
  });
}

function getSqlTooltipElement() {
  if (sqlTooltipElement) {
    return sqlTooltipElement;
  }

  sqlTooltipElement = document.createElement('div');
  sqlTooltipElement.className = 'sql-floating-tooltip';
  sqlTooltipElement.innerHTML = `
    <div class="sql-tooltip-header">
      <span>SQL_FULLTEXT</span>
      <small>Consulta executada no Oracle</small>
    </div>
    <pre class="sql-tooltip-code"></pre>
  `;

  document.body.appendChild(sqlTooltipElement);

  return sqlTooltipElement;
}

function showSqlTooltip(event) {
  const element = event.currentTarget;
  const tooltip = getSqlTooltipElement();

  const encodedSql = element.getAttribute('data-sql-fulltext') || '';
  const sqlFullText = decodeURIComponent(encodedSql);

  const codeElement = tooltip.querySelector('.sql-tooltip-code');
  codeElement.textContent = formatSqlForDisplay(sqlFullText);

  tooltip.classList.add('visible');

  moveSqlTooltip(event);
}

function showSqlTooltipByFocus(event) {
  const element = event.currentTarget;
  const tooltip = getSqlTooltipElement();

  const encodedSql = element.getAttribute('data-sql-fulltext') || '';
  const sqlFullText = decodeURIComponent(encodedSql);

  const codeElement = tooltip.querySelector('.sql-tooltip-code');
  codeElement.textContent = formatSqlForDisplay(sqlFullText);

  tooltip.classList.add('visible');

  const rect = element.getBoundingClientRect();

  positionSqlTooltip({
    clientX: rect.left,
    clientY: rect.bottom
  });
}

function moveSqlTooltip(event) {
  positionSqlTooltip(event);
}

function positionSqlTooltip(event) {
  const tooltip = getSqlTooltipElement();

  const padding = 16;
  const offset = 16;

  let left = event.clientX + offset;
  let top = event.clientY + offset;

  const rect = tooltip.getBoundingClientRect();

  if (left + rect.width + padding > window.innerWidth) {
    left = event.clientX - rect.width - offset;
  }

  if (top + rect.height + padding > window.innerHeight) {
    top = window.innerHeight - rect.height - padding;
  }

  left = Math.max(padding, left);
  top = Math.max(padding, top);

  tooltip.style.left = `${left}px`;
  tooltip.style.top = `${top}px`;
}

function hideSqlTooltip() {
  const tooltip = getSqlTooltipElement();
  tooltip.classList.remove('visible');
}

function formatSqlForDisplay(sql) {
  if (!sql || !String(sql).trim()) {
    return 'SQL não disponível.';
  }

  let text = String(sql)
    .replace(/\s+/g, ' ')
    .trim();

  /*
    Formatação simples para facilitar leitura.
    Não é um parser SQL completo, mas já melhora bastante
    para SELECTs vindos de v$sqlarea/v$sql.
  */
  text = text
    .replace(/\bSELECT\b/gi, 'SELECT\n  ')
    .replace(/\bFROM\b/gi, '\nFROM')
    .replace(/\bWHERE\b/gi, '\nWHERE')
    .replace(/\bGROUP\s+BY\b/gi, '\nGROUP BY')
    .replace(/\bORDER\s+BY\b/gi, '\nORDER BY')
    .replace(/\bHAVING\b/gi, '\nHAVING')
    .replace(/\bUNION\s+ALL\b/gi, '\nUNION ALL')
    .replace(/\bUNION\b/gi, '\nUNION')
    .replace(/\bFETCH\s+FIRST\b/gi, '\nFETCH FIRST')
    .replace(/\bOFFSET\b/gi, '\nOFFSET')
    .replace(/\bINNER\s+JOIN\b/gi, '\nINNER JOIN')
    .replace(/\bLEFT\s+JOIN\b/gi, '\nLEFT JOIN')
    .replace(/\bLEFT\s+OUTER\s+JOIN\b/gi, '\nLEFT OUTER JOIN')
    .replace(/\bRIGHT\s+JOIN\b/gi, '\nRIGHT JOIN')
    .replace(/\bRIGHT\s+OUTER\s+JOIN\b/gi, '\nRIGHT OUTER JOIN')
    .replace(/\bFULL\s+JOIN\b/gi, '\nFULL JOIN')
    .replace(/\bFULL\s+OUTER\s+JOIN\b/gi, '\nFULL OUTER JOIN')
    .replace(/\bJOIN\b/gi, '\nJOIN')
    .replace(/\bON\b/gi, '\n  ON')
    .replace(/\bAND\b/gi, '\n  AND')
    .replace(/\bOR\b/gi, '\n  OR')
    .replace(/\s*,\s*/g, ',\n  ');

  const linhas = text
    .split('\n')
    .map((linha) => linha.trim())
    .filter(Boolean)
    .map((linha) => {
      if (
        linha.startsWith('SELECT') ||
        linha.startsWith('FROM') ||
        linha.startsWith('WHERE') ||
        linha.startsWith('GROUP BY') ||
        linha.startsWith('ORDER BY') ||
        linha.startsWith('HAVING') ||
        linha.startsWith('UNION') ||
        linha.startsWith('FETCH FIRST') ||
        linha.startsWith('OFFSET') ||
        linha.includes('JOIN')
      ) {
        return linha;
      }

      if (
        linha.startsWith('AND') ||
        linha.startsWith('OR') ||
        linha.startsWith('ON')
      ) {
        return `  ${linha}`;
      }

      return `  ${linha}`;
    });

  return linhas.join('\n');
}