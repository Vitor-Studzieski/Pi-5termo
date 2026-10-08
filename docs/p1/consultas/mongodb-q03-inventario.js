// Q03: contagens e cobertura temporal das colecoes historicas do Grupo 2.
// Executar com mongosh conectado ao banco grupo2. Somente leitura.
const nomes = ["leituras", "telemetria_maquinas", "alertas", "imagens"];
for (const nome of nomes) {
  const c = db.getCollection(nome);
  const total = c.countDocuments({});
  // As imagens usam `data`; as outras colecoes usam `ts`.
  const campoData = nome === "imagens" ? "data" : "ts";
  const cobertura = c.aggregate([
    { $group: { _id: null, primeiro: { $min: `$${campoData}` }, ultimo: { $max: `$${campoData}` } } }
  ]).toArray();
  printjson({ colecao: nome, documentos: total, campo_data: campoData, cobertura_utc: cobertura[0] || null });
}

// Distribuicao de leituras por sensor e firmware.
print("Leituras por sensor/firmware:");
printjson(db.leituras.aggregate([
  { $group: { _id: { sensor: "$sensor", firmware: "$firmware" }, n: { $sum: 1 },
              primeiro_utc: { $min: "$ts" }, ultimo_utc: { $max: "$ts" } } },
  { $sort: { "_id.sensor": 1, "_id.firmware": 1 } }
]).toArray());
