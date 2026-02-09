import yaml
import os

def convert_saas():
    base_path = "c:/Users/pedro.possani_capim/ontologia-cf/_domain"
    old_index_path = os.path.join(base_path, "_docs/ENTITY_INDEX.yaml")
    new_index_path = os.path.join(base_path, "_docs/ONTOLOGY_INDEX_SAAS.yaml")
    
    if not os.path.exists(old_index_path):
        print(f"Skipping SAAS: {old_index_path} not found")
        return

    with open(old_index_path, 'r', encoding='utf-8') as f:
        old_index = yaml.safe_load(f)
        
    new_entities = []
    for entity in old_index.get('entities', []):
        name = entity['name']
        
        # Promotion Logic
        if name in ['PATIENTS', 'CLINICS', 'CLINIC_DIM_V1']:
            qid = f"ECOSYSTEM.{name}"
            domains = ["SAAS", "FINTECH"]
        else:
            qid = f"SAAS.{name}"
            domains = ["SAAS"]

        agentic_path = entity.get('original_doc')
        if agentic_path and not agentic_path.startswith('..'):
             agentic_path = os.path.join('..', agentic_path).replace('\\', '/')

        new_entities.append({
            "id": qid,
            "semantic_doc": entity.get('semantic_doc'),
            "agentic_doc": agentic_path,
            "domains": domains,
            "tier": 1 if entity.get('trust_level') == 'CANONICAL' else 2,
            "status": "ACTIVE"
        })
        
    with open(new_index_path, 'w', encoding='utf-8') as f:
        yaml.dump({"entities": new_entities}, f, sort_keys=False)
        
    print(f"✅ Generated SAAS ONTOLOGY_INDEX_SAAS.yaml with Ecosystem promotion.")

def convert_fintech():
    base_path = "c:/Users/pedro.possani_capim/bnpl-funil/_domain"
    old_index_path = os.path.join(base_path, "_docs/ENTITY_INDEX.yaml")
    new_index_path = os.path.join(base_path, "_docs/ONTOLOGY_INDEX_FINTECH.yaml")
    
    if not os.path.exists(old_index_path):
        print(f"Skipping FINTECH: {old_index_path} not found")
        return

    with open(old_index_path, 'r', encoding='utf-8') as f:
        old_index = yaml.safe_load(f)
        
    new_entities = []
    for entity in old_index.get('entities', []):
        name = entity['name']
        
        # Promotion Logic
        if name in ['PATIENTS', 'CLINICS']:
            qid = f"ECOSYSTEM.{name}"
            domains = ["SAAS", "FINTECH"]
        else:
            qid = f"FINTECH.{name}"
            domains = ["FINTECH"]

        agentic_path = entity.get('original_doc')
        if agentic_path and not agentic_path.startswith('..'):
             agentic_path = os.path.join('..', agentic_path).replace('\\', '/')

        new_entities.append({
            "id": qid,
            "semantic_doc": entity.get('semantic_doc'),
            "agentic_doc": agentic_path,
            "domains": domains,
            "tier": 1 if entity.get('trust_level') == 'CANONICAL' else 2,
            "status": "ACTIVE"
        })
        
    with open(new_index_path, 'w', encoding='utf-8') as f:
        yaml.dump({"entities": new_entities}, f, sort_keys=False)
        
    print(f"✅ Generated FINTECH ONTOLOGY_INDEX_FINTECH.yaml with Ecosystem promotion.")

if __name__ == "__main__":
    convert_saas()
    convert_fintech()
