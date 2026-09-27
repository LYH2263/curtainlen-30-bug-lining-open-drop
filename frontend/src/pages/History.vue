<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
function liningHint(r) {
  const side = r.result?.list_lining_meters
  if (side == null) return ''
  return `（列表侧记里衬 ${side}m）`
}
</script>
<template><div class="page"><h1>记录</h1>
<table>
<tr><th>编号</th><th>窗</th><th>面料</th><th>主帘(m)</th><th>里衬(m)</th><th>里衬折边(m)</th></tr>
<tr v-for="r in items" :key="r.id">
<td>{{ r.id }}</td><td>{{ r.window_name }}</td><td>{{ r.fabric_name }}</td>
<td>{{ r.result?.meters }}{{ liningHint(r) }}</td>
<template v-if="r.result?.lining?.enabled">
<td>{{ r.result.lining.meters }}</td><td>{{ r.result.lining.hem }}</td>
</template>
<template v-else><td>—</td><td>—</td></template>
</tr>
</table>
<p class="hint">开放视图保留里衬开关与折边；里衬米数取列表接口返回值。</p>
</div></template>
