-- Q01: contagem exata de linhas por tabela do schema grupo2.
-- Executar conectado ao banco grupo2. Somente leitura.
SELECT 'fazenda' AS tabela, COUNT(*) AS linhas FROM fazenda
UNION ALL SELECT 'talhao', COUNT(*) FROM talhao
UNION ALL SELECT 'cultura', COUNT(*) FROM cultura
UNION ALL SELECT 'safra', COUNT(*) FROM safra
UNION ALL SELECT 'sensor', COUNT(*) FROM sensor
UNION ALL SELECT 'maquina', COUNT(*) FROM maquina
UNION ALL SELECT 'funcionario', COUNT(*) FROM funcionario
UNION ALL SELECT 'insumo', COUNT(*) FROM insumo
UNION ALL SELECT 'operacao', COUNT(*) FROM operacao
UNION ALL SELECT 'estoque_movimento', COUNT(*) FROM estoque_movimento
UNION ALL SELECT 'cliente', COUNT(*) FROM cliente
UNION ALL SELECT 'venda', COUNT(*) FROM venda
ORDER BY tabela;
