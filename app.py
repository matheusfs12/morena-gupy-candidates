import streamlit as st
import requests

def fetch_candidates(token: str, job_step_filter: str):
    """
    Realiza as requisições paginadas para a API da Gupy e retorna uma lista de dicionários contendo:
    - URL do candidato
    - Nome completo (candidate.name + candidate.lastName)
    
    Filtra os candidatos cujo jobStep.name corresponde ao filtro informado.
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
        
        # Em caso de erro, exibe a mensagem e interrompe o loop
        if response.status_code != 200:
            st.error(f"Erro na requisição (Status {response.status_code}): {response.text}")
            break
        
        json_data = response.json()
        
        # Se não houver dados na página, encerra o loop
        if "data" not in json_data or not json_data["data"]:
            break
        
        # Itera sobre os itens da página filtrando pelo jobStep.name
        for item in json_data["data"]:
            job_step = item.get("jobStep")
            if job_step and job_step.get("name") == job_step_filter:
                candidate_info = item.get("candidate", {})
                candidate_name = candidate_info.get("name", "")
                candidate_last_name = candidate_info.get("lastName", "")
                full_name = f"{candidate_name} {candidate_last_name}".strip()
                candidate_url = f"https://compass.gupy.io/companies/jobs/7424813/candidates/{item.get('id')}"
                results.append({
                    "url": candidate_url,
                    "name": full_name
                })
        
        # Verifica se há mais páginas disponíveis
        summary = json_data.get("summary")
        if summary and summary.get("pageCount") is not None:
            if page >= summary.get("pageCount") - 1:
                break
        
        # Se a quantidade de registros retornados for menor que per_page, encerra o loop
        if len(json_data["data"]) < per_page:
            break
        
        page += 1

    return results

def main():
    st.title("Filtrador de Candidatos - Gupy API")
    st.write("Este app consulta a API da Gupy, filtrando candidatos pelo campo `jobStep.name`.")

    # Entradas do usuário
    token = st.text_input("Token de autenticação (company_key_auth)")
    job_step_filter = st.text_input("Job Step Name para filtrar", value="Entrevista Técnica")

    if st.button("Buscar Candidatos"):
        if not token or not job_step_filter:
            st.warning("Por favor, informe o token e o Job Step Name.")
        else:
            with st.spinner("Realizando requisições..."):
                candidates = fetch_candidates(token, job_step_filter)
            
            if candidates:
                st.success(f"Foram encontrados {len(candidates)} candidatos com o jobStep.name '{job_step_filter}'.")
                st.write("Candidatos encontrados:")
                for candidate in candidates:
                    st.write(f"**Nome:** {candidate['name']}  \n**URL:** {candidate['url']}")
            else:
                st.info("Nenhum candidato encontrado com o jobStep.name informado.")

if __name__ == '__main__':
    main()