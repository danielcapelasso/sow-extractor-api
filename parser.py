from docx import Document
import io
import re

def extract_sow_data(file_bytes):
    document = Document(io.BytesIO(file_bytes))

    data = {
        "consultor_responsavel": None,
        "contexto_projeto": None,
        "etapas_projeto": None,
        "tempo_estimado": None,
        "principais_regras_negocio": [],
        "resumo_servicos": [],
        "casos_de_uso_detalhados": []
    }

    for i, table in enumerate(document.tables):
        # Novo formato: tabela com tipo, regra, descrição, comentário, atendido
        headers = [cell.text.strip().lower() for cell in table.rows[0].cells]
        if "tipo" in headers and "regra" in headers:
            for row in table.rows[1:]:
                cells = row.cells
                try:
                    tipo = cells[0].text.strip()
                    regra = cells[1].text.strip()
                    descricao = cells[2].text.strip() if len(cells) > 2 else ""
                    comentario = cells[3].text.strip() if len(cells) > 3 else ""
                    atendido = cells[4].text.strip().upper() if len(cells) > 4 else ""
                    data["principais_regras_negocio"].append({
                        "tipo": tipo,
                        "regra": regra,
                        "descricao": descricao,
                        "comentario": comentario,
                        "atendido": atendido
                    })
                except Exception:
                    continue

        # Resumo de serviços (modelo antigo)
        elif "serviço" in headers[0].lower():
            for row in table.rows[1:]:
                cells = row.cells
                if len(cells) >= 2:
                    data["resumo_servicos"].append({
                        "serviço": cells[0].text.strip(),
                        "detalhes": cells[1].text.strip()
                    })

    # Pega textos soltos do documento
    full_text = "\n".join([p.text for p in document.paragraphs])

    # Padrões simples baseados no texto
    match = re.search(r"Consultor Responsável: (.+)", full_text)
    if match:
        data["consultor_responsavel"] = match.group(1).strip()

    match = re.search(r"Objetivo Geral[:\-]?\s*(.+)", full_text)
    if match:
        data["contexto_projeto"] = match.group(1).strip()

    match = re.search(r"Etapas do Projeto[:\-]?\s*(.+)", full_text)
    if match:
        data["etapas_projeto"] = match.group(1).strip()

    match = re.search(r"Tempo Estimado[:\-]?\s*(.+)", full_text)
    if match:
        data["tempo_estimado"] = match.group(1).strip()

    return data










