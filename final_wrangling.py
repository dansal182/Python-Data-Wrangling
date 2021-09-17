import numpy as np
import pandas as pd
from merge_end_samp import fx_cve
from datos_drogas import fix_cve, mun_join


def load_files(f_names):
    files = []
    for f in f_names:
        files.append(pd.read_csv(dir_end.replace('/municipal', '') + '/' + f.replace('.csv', '_muestra.csv')))
    return files


def get_file_names(f_names, new_name):
    out = []
    for f in f_names:
        out.append(f.replace('.csv', new_name))
    return out


def create_samples(sam_key, files, f_names):
    s_files = []
    s_names = get_file_names(f_names, '_muestra.csv')
    for file in files:
        s_files.append(pd.merge(sam_key, file, on='cve_unica', how='inner'))
    save_files(s_files, s_names)
    return 0


def save_files(files, f_names):
    for i, f in enumerate(files):
        f.to_csv(dir_end + '/' + f_names[i], index=False)


def create_mun_strata(mun_key, files, f_names):
    m_names = get_file_names(f_names, '_muestra_nivMunicipal.csv')
    m_files = []
    for file in files:
        if 'cve_unica' in file.columns:
            aux = pd.merge(mun_key[['cve_unica', 'cve_entmun']], file, on='cve_unica')
            m_files.append(mun_join(aux, aux.columns.drop('cve_unica'), 'cve_entmun'))
    save_files(m_files, m_names)
    return 0


dir_end = '/Users/danielsalnikov/Documents/Ejidos/bases_finales/muestras/municipal'
# land = fx_cve(pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/recur_natur/uso_tierra_renatur_ecosistema.csv'),
#               ['Clv_Ejido', 'cve_unica'], '*')
# aa = fx_cve(pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/otras_bases/otras_final/aa_nejd_qaunt.csv'),
#             ['Clv_Ejido', 'cve_unica'], '*')
# sj = fx_cve(pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/otras_bases/otras_final/suj_ejd.csv'),
#             ['Clv_Ejido', 'cve_unica'], '*')
# pr = fx_cve(pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/otras_bases/otras_final/trasp_pleno_nivej.csv'),
#             ['Clv_Ejido', 'cve_unica'], '*')
# aa_date = fx_cve(
#     pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/bases_finales/acciones_agrarias_serie_de_tiempo.csv'),
#     ['cve_unica', 'cve_unica'], '*')
# vote_ts_sec = pd.read_csv(
#     '/Users/danielsalnikov/Documents/Ejidos/elecciones/bases_finales/time_series/time_series_91_21.csv')
# key_elec = pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/elecciones/bases_finales/2021/llave_secciones.csv')
# vote_ts_ejd = fx_cve(
#     pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/elecciones/bases_finales/time_series/time_series_ejidos.csv'),
#     ['Clv_Unica', 'cve_unica'], '*')
# vote_panel = fx_cve(pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/elecciones/bases_finales/'
#                                 'pan_elecc_ejidos_edit.csv', dtype={'Clv_Ejido': 'str', 'Elecc': 'str'}),
#                     ['Clv_Ejido', 'cve_unica'], '*')
# key_entmun = fx_cve(pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/uso_de_tierra/nucleos/clv_ejd_mun.csv'),
#                     ['Clv_Ejido', 'cve_unica'], '*')
# key_entmun = fix_cve(key_entmun, 'cve_entmun')
# archives = [land, aa, pr, sj, aa_date, vote_ts_sec, vote_ts_ejd, vote_panel, key_entmun]
# sample_key = pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/bases_finales/muestras/muestra_PA3_llave.csv')
mun_key = pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/bases_finales/clv_ejd_mun.csv')
ar_names = ['uso_tierra_renatur_ecosistema.csv', 'aa_nejd_qaunt.csv', 'trasp_pleno_nivej.csv', 'suj_ejd.csv',
            'acciones_agrarias_serie_de_tiempo.csv', 'time_series_ejidos.csv']
# save_files(archives, ar_names)
arhvs = load_files(ar_names)
# create_samples(sample_key, arhvs, ar_names)
create_mun_strata(mun_key, arhvs, ar_names)
