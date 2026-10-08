-- Q02: custo e volume por tipo de operacao. Somente leitura.
SELECT tipo,
       COUNT(*) AS quantidade,
       ROUND(SUM(custo_total), 2) AS custo_total,
       ROUND(AVG(custo_total), 2) AS custo_medio
FROM operacao
GROUP BY tipo
ORDER BY custo_total DESC;

-- Q02b: produtividade registrada por talhao na safra colhida 2025/26.
SELECT t.codigo AS talhao,
       c.nome AS cultura,
       s.produtividade_kg_ha
FROM safra s
JOIN talhao t ON t.id = s.talhao_id
JOIN cultura c ON c.id = s.cultura_id
WHERE s.ano_safra = '2025/26' AND s.status = 'colhida'
ORDER BY s.produtividade_kg_ha DESC;
