from eutilities.string_utils import jaccard_similarity, stem_phrase
from myio.data_reader import DBReader


def print_info(df):
    print('shape: ', df.shape)
    print(df.head(3))


df_wos_keyword = DBReader.cached_read('cached/ontology/wos_keyword.pkl', 'SELECT * FROM medical_informatics.wos_keyword;',
                                      cached=True)
df_wos_keyword['keyword'] = df_wos_keyword['keyword'].apply(stem_phrase)
print_info(df_wos_keyword)

df_cso = DBReader.cached_read('cached/ontology/cso_unique_concept.pkl', 'SELECT * FROM medical_informatics.cso_unique_concept;',
                              cached=True)
df_cso['concept'] = df_cso['concept'].apply(stem_phrase)
print_info(df_cso)

df_mesh = DBReader.cached_read('cached/ontology/pubmed_mesh.pkl', 'SELECT * FROM pr.mesh_id_keyword_map;', cached=True)
df_mesh['mesh_keyword'] = df_mesh['mesh_keyword'].apply(stem_phrase)
print_info(df_mesh)


def match_ontolopy(arr, df):
    mesh_sim_arr = []
    # for k, (cso_original_ontology, concept) in df_cso.iterrows():
    for j, (mesh_id, mesh_keyword) in df.iterrows():
        sim = jaccard_similarity(arr, mesh_keyword.lower().split(' '))
        mesh_sim_arr.append([mesh_id, mesh_keyword, sim])
    mesh_sim_arr = sorted(mesh_sim_arr, key=lambda x: -1.0 * x[-1])
    return mesh_sim_arr


for i, (keyword_id, document_unique_id, keyword) in df_wos_keyword.iterrows():
    # match for each keyword
    l1 = keyword.lower().split(' ')
    # most_sim_ontology = match_ontolopy(l1, df_mesh)
    most_sim_ontology = match_ontolopy(l1, df_cso)
    print(keyword, '#' * 10, most_sim_ontology[:10])
