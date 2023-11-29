import sys
import pickle
import numpy as np

# Captura argumentos da linha de comando
v = str(sys.argv[1])        # versão simulação
batch = sys.argv[2]         # batch simulações
subbatch = sys.argv[3]      # subbatch (simulação)
i = int(sys.argv[4])             # indice para inserir no array

# Formata números para garantir quatro dígitos em batch_number
batch_number = 'batch' + str(batch.zfill(4))
subbatch_number = '0_' + str(subbatch)

# Gera o caminho do arquivo com base nos argumentos
file = f'../data/v{v}_{batch_number}/v{v}_{batch_number}_{subbatch_number}'

# Exibe mensagem indicando o arquivo que está sendo lido
print(f'~ Read file: {file}')

# Abre o arquivo e carrega os resultados usando pickle
with open(file + '_data.pkl', 'rb') as f:
    arq_resultados = pickle.load(f)

# Extrai variáveis específicas dos resultados
gex = arq_resultados['simConfig']['gex']
amp = arq_resultados['simConfig']['IClamp0']['amp']
neighbours = arq_resultados['simConfig']['n_neighbors']
mean_GOP = arq_resultados['GOP'].mean()
mean_LOP = arq_resultados['LOP_delta'][5].mean(axis=1).mean()
mean_freq = np.mean(arq_resultados['freq_bar'])
mean_cv = np.mean(arq_resultados['cv'])

# Tenta abrir o arquivo de espaço de parâmetros, cria um novo se não existir
try:
    with open(f'../data/space_param_V{v}.pkl', 'rb') as f:  # Modificado 'wb' para 'rb'
        space_param = pickle.load(f)
except EOFError:
    print('===== Erro EOF! =====')
    with open('../data/log_error_readpickle.txt', 'a') as log:
        log.writelines(f'error open: {file}')

# Adiciona os dados extraídos ao dicionário space_param
space_param['gex'][i] = gex
space_param['amp'][i] = amp
space_param['neighbours'][i] = neighbours
space_param['mean_GOP'][i] = mean_GOP
space_param['mean_LOP'][i] = mean_LOP
space_param['mean_freq'][i] = mean_freq
space_param['mean_cv'][i] = mean_cv

# Exibe mensagem indicando que o arquivo pickle está sendo salvo
print(f'~ Dump pickle file: ../data/space_param_V{v}.pkl')

# Salva o dicionário atualizado em um arquivo pickle
with open(f'../data/space_param_V{v}.pkl', 'wb') as handle:
    pickle.dump(space_param, handle, protocol=pickle.HIGHEST_PROTOCOL)

del arq_resultados
del space_param
print('\n')
