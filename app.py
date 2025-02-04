import streamlit as st
import requests

def fetch_candidates(token: str, job_step_filter: str):
    """
    Realiza as requisições paginadas para a API da Gupy e retorna uma lista de URLs dos candidatos
    cujo jobStep.name corresponde ao filtro informado.
    """
    base_url = "https://private-api.gupy.io/selection-process/company/job/7424813/application"
    headers = {
        "company_key_auth": token,
        "accept": "application/json",
        "content-type": "application/json",
    }
    
    results = []
    page = 0
    per_page = 50
    
    while True:
        params = {
            "page": page,
            "perPage": per_page,
            "status": "reproved",
            "order": "!affinity",  # !affinity equivale a \u0021affinity
        }
        
        response = requests.get(base_url, headers=headers, params=params)
        
        # Se houver erro na requisição, interrompe o loop
        if response.status_code != 200:
            st.error(f"Erro na requisição (Status {response.status_code}): {response.text}")
            break
        
        json_data = response.json()
        
        # Se não houver dados na página, encerra o loop
        if "data" not in json_data or not json_data["data"]:
            break
        
        # Para cada item da página, verifica se o campo jobStep.name bate com o filtro
        for item in json_data["data"]:
            job_step = item.get("jobStep")
            if job_step and job_step.get("name") == job_step_filter:
                # Monta a URL do candidato usando o campo "id" do item
                candidate_url = f"https://compass.gupy.io/companies/jobs/7424813/candidates/{item.get('id')}"
                results.append(candidate_url)
        
        # Verifica se há mais páginas. Se houver "summary" com pageCount, usa-o para parar.
        summary = json_data.get("summary")
        if summary and summary.get("pageCount") is not None:
            if page >= summary.get("pageCount") - 1:
                break
        
        # Se a quantidade de registros retornados for menor que o perPage, provavelmente chegou à última página
        if len(json_data["data"]) < per_page:
            break
        
        page += 1

    return results

def main():
    st.title("Filtrador de Candidatos - Gupy API")
    st.write("Este app consulta a API da Gupy, filtrando candidatos pelo campo `jobStep.name`.")

    # Entrada de dados
    token = st.text_input("Token de autenticação (company_key_auth)", type="password")
    job_step_filter = st.text_input("Job Step Name para filtrar")

    if st.button("Buscar Candidatos"):
        if not token or not job_step_filter:
            st.warning("Por favor, informe o token e o Job Step Name.")
        else:
            with st.spinner("Realizando requisições..."):
                candidate_urls = fetch_candidates(token, job_step_filter)
            
            if candidate_urls:
                st.success(f"Foram encontrados {len(candidate_urls)} candidatos com o jobStep.name '{job_step_filter}'.")
                st.write("URLs dos candidatos:")
                for url in candidate_urls:
                    st.write(url)
            else:
                st.info("Nenhum candidato encontrado com o jobStep.name informado.")

if __name__ == '__main__':
    main()