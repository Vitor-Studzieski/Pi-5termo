// Q07: triagem de defeitos em leituras. Executar no MongoDB do Grupo 2.
// Somente leitura; os limiares sao criterios de triagem e precisam de validacao.
const c = db.leituras;
const duplicatas = c.aggregate([
  { $group: { _id: { sensor: "$sensor", ts: "$ts" }, n: { $sum: 1 } } },
  { $match: { n: { $gt: 1 } } },
  { $group: { _id: null, chaves_duplicadas: { $sum: 1 }, linhas_excedentes: { $sum: { $subtract: ["$n", 1] } } } }
]).toArray();
printjson({ duplicatas: duplicatas[0] || { chaves_duplicadas: 0, linhas_excedentes: 0 } });

const percentuaisInvalidos = c.countDocuments({ $or: [
  { "valores.umidade_10cm_pct": { $lt: 0 } }, { "valores.umidade_10cm_pct": { $gt: 100 } },
  { "valores.umidade_30cm_pct": { $lt: 0 } }, { "valores.umidade_30cm_pct": { $gt: 100 } },
  { "valores.umidade_pct": { $lt: 0 } }, { "valores.umidade_pct": { $gt: 100 } },
  { bateria_pct: { $lt: 0 } }, { bateria_pct: { $gt: 100 } }
] });
printjson({ percentuais_fora_de_0_a_100: percentuaisInvalidos });

// Escala dos valores por sensor/firmware para investigar troca de unidade.
print("Escala de umidade por sensor/firmware (quando o campo existe):");
printjson(c.aggregate([
  { $match: { "valores.umidade_10cm_pct": { $exists: true, $type: "number" } } },
  { $group: { _id: { sensor: "$sensor", firmware: "$firmware" }, n: { $sum: 1 },
              minimo: { $min: "$valores.umidade_10cm_pct" },
              maximo: { $max: "$valores.umidade_10cm_pct" },
              media: { $avg: "$valores.umidade_10cm_pct" } } },
  { $sort: { "_id.sensor": 1, "_id.firmware": 1 } }
]).toArray());

// Indicador da ordem natural de armazenamento versus hora de evento por sensor.
const ultimoPorSensor = new Map();
const foraDeOrdem = new Map();
for (const doc of c.find({}, { _id: 0, sensor: 1, ts: 1 }).sort({ $natural: 1 })) {
  const ms = new Date(doc.ts).getTime();
  const anterior = ultimoPorSensor.get(doc.sensor);
  if (anterior !== undefined && ms < anterior) {
    foraDeOrdem.set(doc.sensor, (foraDeOrdem.get(doc.sensor) || 0) + 1);
  }
  ultimoPorSensor.set(doc.sensor, ms);
}
printjson({ documentos_fora_de_ordem_natural_por_sensor: Object.fromEntries(foraDeOrdem),
            observacao: "ordem natural e indicador; ts e a hora de evento" });

// Lacunas: historico de sensores tem cadencia nominal de 15 minutos.
const porSensor = c.find({}, { _id: 0, sensor: 1, ts: 1, firmware: 1, valores: 1 })
  .sort({ sensor: 1, ts: 1 }).toArray();
const estados = new Map();
const lacunas = new Map();
const repeticoesLongas = new Map();
for (const doc of porSensor) {
  const ms = new Date(doc.ts).getTime();
  const previo = estados.get(doc.sensor);
  if (previo) {
    const delta = ms - previo.ms;
    if (delta > 15 * 60 * 1000) {
      const faltantes = Math.max(1, Math.floor(delta / (15 * 60 * 1000)) - 1);
      lacunas.set(doc.sensor, (lacunas.get(doc.sensor) || 0) + faltantes);
    }
    const atual = JSON.stringify(doc.valores || {});
    const seq = atual === previo.fingerprint ? previo.repeticoes + 1 : 1;
    if (seq >= 8) repeticoesLongas.set(doc.sensor, (repeticoesLongas.get(doc.sensor) || 0) + 1);
    estados.set(doc.sensor, { ms, fingerprint: atual, repeticoes: seq });
  } else {
    estados.set(doc.sensor, { ms, fingerprint: JSON.stringify(doc.valores || {}), repeticoes: 1 });
  }
}
printjson({ intervalos_faltantes_estimados_por_sensor: Object.fromEntries(lacunas),
            ocorrencias_em_sequencias_de_8_ou_mais: Object.fromEntries(repeticoesLongas),
            criterio_lacuna: "timestamp consecutivo acima de 15 min; UTC" });
