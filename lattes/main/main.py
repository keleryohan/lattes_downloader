import os
from bs4 import BeautifulSoup as BS
import lattes.soup.full_articles_manager as FULLARTS
import lattes.soup.full_works_manager as FULLWORKS
import lattes.soup.exam_commissions_manager as EXAMCOMMISSIONS
import lattes.soup.editorial_member_manager as EDITORIALMEMBER
import lattes.soup.journal_reviewer_manager as EDITORIALREVIEWER
import lattes.soup.researcher_project_manager as RESEARCPROJECTS
from lattes.excel.xl import XL
#Identificação
#Formação acadêmica/titulação
#Pós-doutorado e Livre-docência
#Atuação Profissional
#Linhas de pesquisa
#Projetos de pesquisa
#Membro de corpo editorial ------- ok
#Revisor de periódico >>>>>
#Áreas de atuação
#Idiomas
#Prêmios e títulos
#Artigos completos publicados em periódicos ------- ok
#Livros publicados/organizados ou edições
#Capítulos de livros publicados
#Trabalhos completos publicados em anais de congressos -------- ok
#--Participação em bancas de trabalhos de conclusão  -------- ok
##Mestrado  -------- ok
##Teses de doutorado  -------- ok
##Qualificações de Doutorado  -------- ok
##Qualificações de Mestrado  -------- ok
##Trabalhos de conclusão de curso de graduação  -------- ok
##--Outros tipos  -------- ok
#--Participação em bancas de comissões julgadoras  -------- ok
##Concurso público  -------- ok
##Outras participações  -------- ok
#--Eventos
##Participação em eventos, congressos, exposições e feiras
##Organização de eventos, congressos, exposições e feiras
#Orientações
#--Orientações e supervisões em andamento
#Dissertação de mestrado
#--Orientações e supervisões concluídas
##Dissertação de mestrado
##Tese de doutorado
##Iniciação científica
#Inovação
#Projetos de pesquisa


def get_BS(arquivo):
    #b 0: verificando se o arquivo é um arquivo .nk
    if not arquivo.endswith(".html"):
        print(f'Arquivo {arquivo} não é um arquivo ".html"!')
        return None
    #e 0: se o arquivo não é um arquivo .nk, retorna vazio



    #b 1: criando um BS; se houver erro na leitura do .nk retorna vazio
    try:
        arquivo_para_ler = open(arquivo,"rb")
        bs = BS(arquivo_para_ler.read().decode("latin8"),"html.parser")
        arquivo_para_ler.close()
    except Exception as e:
        print("ERRO!",e)
        return None
    else:
        return bs
    #e 1: BS criado como "bs"






def pega_arquivo_nk_e_faz_tudo(arquivo): #arquivo .nk
    #b 0: pegando BS do arquivo
    bs = get_BS(arquivo)
    #e 0: um beaultifulSoup foi gerado


    #b 1: obtendo a lista de artigos completos
    itens_fullarts = FULLARTS.get_itens(bs)

    #e 1: o resultado é uma lista de "Item"

    #b 2: obtendo a lista de trabalhos completos
    itens_fullworks = FULLWORKS.get_itens(bs)
    #e 2: o resultado é uma lista de "Item"

    #b 2.1 obtendo a lista de bancas
    itens_exam_commissions = EXAMCOMMISSIONS.get_itens(bs)
    #e 2.1

    #b 2.2
    itens_editorial_member = EDITORIALMEMBER.get_itens(bs)
    #e 2.2

    #b 2.3
    itens_editorial_reviewer = EDITORIALREVIEWER.get_itens(bs)
    #e 2.3

    #b 2.4
    itens_projeto_pesquisa = RESEARCPROJECTS.get_itens(bs)
    #e 2.4

    #b 2: criar uma planilha com os itens
    EXCEL = XL(arquivo)
    EXCEL.artigos_completos(
                itens_fullarts,
                )

    EXCEL.trabalhos_completos(
                itens_fullworks,
                )
    ####################################!!!!!!!!ADICIONAR AQUI
    EXCEL.bancas(
                itens_exam_commissions,
                )
    EXCEL.membro_editorial(
                itens_editorial_member
                )
    EXCEL.revisor_de_periodico(
                itens_editorial_reviewer
                )
    EXCEL.projetos_pesquisa(
                itens_projeto_pesquisa
                )

    EXCEL.save()
    #return itens_artigos_completos_publicados_em_periodicos
    #e 2:














def processar_arquivos_pastas_e_gerar_planilhas():
    #path até a pasta de downloads
    path = "../../paginas_lattes_aqui"

    #b 0: listando todos os arquivos html na pasta atual
    lista_de_arquivos_html = filter(lambda x: x.endswith(".html"), os.listdir(path))
    
    
    #e 0: retorna uma lista de strings, os nomes dos arquivos


    #b 1: renomeando os arquivos: a extensão .html será alterada para .nk
    for arquivo in lista_de_arquivos_html:
        #print("1")
        try:
            nome = arquivo.split("(")[1].split(")")[0].replace(" ","_") + ".html"
            os.rename(arquivo, nome)
        except:
            pass
    #e 1: o nome do arquivo será o nome entre parênteses, com _ no lugar de
    #e 1:                                                           espaços
    #e 1: Exemplo:
    #e 1:   'Currículo do Sistema de Currículos Lattes (Junior Rodrigues Ribeiro).html'
    #e 1: passa a ser Junior_Rodrigues_Ribeiro.nk


    #b 2: listando os arquivos .nk presentes na pasta atual
    lista_de_arquivos_nk = filter(lambda x: x.endswith(".html"), os.listdir(path))
    #e 2: uma lista de strings, os nomes dos arquivos.



    #b *: deletando todas as demais pastas
    pastas = list(os.walk("."))[0][1]
    try:
        pastas.remove(".git")
    except:
        pass
    #for pasta in pastas:
    #    os.system('rm -r "' + pasta + '"')
    #e *: todas as pastas serão deletadas


    #b 3: iterando sobre a lista de arquivos .nk
    for arquivo in lista_de_arquivos_nk:
        pega_arquivo_nk_e_faz_tudo(arquivo)
    #e 3: uma planilha excel será gerada para cada arquivo .html

    movendo_planilhas_para_pasta()



def movendo_planilhas_para_pasta():
    #listando arquivos na pasta atual que terminam com .xls (planilhas)
    lista_de_arquivos_xml = filter(lambda x: x.endswith(".xls"), os.listdir())

    for arquivo in lista_de_arquivos_xml:
        #print("1")
        os.rename("./"+arquivo,"../../planilhas_geradas_aqui/"+arquivo)






