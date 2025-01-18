# prompt: gere um código que lê as entradas do usuário e retorna o preço de venda em um streamlit

import streamlit as st
import pickle
import pandas as pd
import sklearn
import xgboost

# Carrega o modelo treinado
try:
    model = pickle.load(open('housing_price_model_xgb.pkl', 'rb'))
except FileNotFoundError:
    st.error("Erro: Arquivo 'housing_price_model.pkl' não encontrado. Certifique-se de que o modelo foi treinado e salvo corretamente.")
    st.stop()

st.title('Predição de Preço de Venda de Imóveis')

bairros_lista = ['Jardim da Saúde','Vila Santa Teresa (Zona Sul)','Bela Vista','Vila Olímpia','Paraíso','Vila Uberabinha','Pinheiros','Vila Santa Clara','Vila Formosa','Aclimação','Vila Andrade','Jardim Aeroporto','Santana','Vila Moinho Velho','Cidade Mãe do Céu','Sacomã','Bosque da Saúde','Vila Gomes','Cidade Monções','Campo Grande','Vila Pompeia','Jardim Marajoara','Campo Belo','Lapa','Jardim Umarizal','Vila Dom Pedro I','Jardim Monte Azul','Jardim Nove de Julho','Móoca','Jardim Japão','Jardim Guarujá','Vila Alpina','Tatuapé','Jardim Iracema','Vila Regina','Jardim Guedala','Consolação','Brooklin','Vila Sofia','Jardim Paulista','Ipiranga','Indianópolis','Cidade Satélite Santa Bárbara','Jardim Sao Paulo','Várzea de Baixo','Campos Eliseos','Cidade São Francisco','Vila Leopoldina','Vila Nivi','Parque das Paineiras','Tremembé','Jardim Macedônia','Moema','Jardim Catarina','Jardim Leonor Mendes de Barros','Tucuruvi','Jardim Taquaral','Vila Liviero','Jardim Dom José','Vila Antonieta','Perdizes','Jardim Umuarama','Vila Mendes','Cerqueira César','Chácara Santo Antônio','Saúde','Jardins','Jardim Dom Bosco','Jardim Casablanca','Parque São Lucas','Alto da Boa Vista','Vila Vera','Vila Emir','Itaim Bibi','Jardim Brasil (Zona Norte)','Jardim Germânia','Jardim Íris','Vila Maria Alta','Mooca','Jardim Santa Cruz','Parque Novo Mundo','Vila Suzana','Vila Ipojuca','Jardim São Paulo','Chora Menino','Vila Mariana','Jardim Ampliação','Barra Funda','Artur Alvim','Butantã','Morumbi','Vila Congonhas','Jardim Caravelas','Jardim Tupi','Jardim Popular','Cambuci','Jabaquara','Jardim América','Jardim Santa Cruz (Campo Grande)','Jardim Vila Formosa','Higienópolis','Penha','Jardim America','Cidade Mae do Ceu','Vila Maria','Vila Clementino','Vila Campestre','Vila Carrão','Jardim da Saude','Vila Mascote','Brás','Vila Romana','Jardim Vergueiro','Paraisópolis','Parque Fongaro','Parque Fernanda','Vila Califórnia','Socorro','Parque Mandaqui','Pedreira','Parque Residencial Cocaia','Parque Bristol','Vila Vermelha','Parque Reboucas','Limão','Vila Nova Curuca','Sumarezinho','Jardim Floresta','Vila Carmosina','Vila Regente Feijó','Faria Lima','Vila Nova Conceição','Chacara Itaim','Vila Nova Parada','Jardim das Vertentes','Santo Amaro','Parque Munhoz','Rio Pequeno','Planalto Paulista','Vila Esperança','Chácara Belenzinho','Jardim Tietê','Várzea da Barra Funda','Vila Constancia','Jardim Ester','Americanópolis','Chácara Santa Maria','Brooklin Paulista','São Paulo','Jardim Leonor','Fazenda Morumbi','Jardim Maria Virgínia','Vila Guilherme','Jaraguá','Campininha','Avenida Mário Lopes Leão','Parque São Jorge','Jardim Parque Morumbi','Vila Beatriz','Vila Minerva','Parque Terceiro Lago','Centro','Jardim São Luís','Jardim Colombo','Jardim Santa Emília','Jardim Celeste','Jardim Alvorada (Zona Oeste)','Nossa Senhora do O','Jurubatuba','Vila Paulo Silas','Liberdade','Vila Graciosa','Jardim Sabara','Vila Santana','Parada Inglesa','Água Fria','Parque São Luís','Santa Cecilia','Água Branca','Caxingui','Jardim das Bandeiras','Alto da Lapa','Mirandópolis','Jardim Prudência','Vila Prado','República','Parque Ipê','Vila Regente Feijo','Jardim Virginia Bianca','Berrini','Jardim Ana Rosa','Jardim Bonfiglioli','Jardim Anhanguera','Parque do Morumbi','Jd Umuarama','Jardim Ester Yolanda','Jardim Santo Elias','Vila Butantã','Vila Palmeiras','Conjunto Residencial José Bonifácio','Vila São Francisco','Vila Isa','Vila São Pedro','Parque Tomas Saraiva','Parque Casa de Pedra','Vila Bertioga','Chac. São Antônio','Jardim Santa Efigênia','Parque Vitória','Vila Prudente','Interlagos','Vila Antônio','Jaguare','Vila Mariza Mazzei','Chácara Santo Antônio (Zona Leste)','Vila Ester (Zona Norte)','Carandiru','Santa Cecília','Campos Elíseos','Vila Leonor','Vila Nova Galvão','Vila Aurora (Zona Norte)','Sumaré','Vila Alexandria','Lauzane Paulista','Cidade Jardim','Vila Ede','Vila Ré','Chácara Santo Antônio (Zona Sul)','Jardim das Acácias','Paraíso do Morumbi','Vila Cruzeiro','Cerq Cesar','Jardim Londrina','Vila Prel','Vila Nova Mazzei','Jardim Monte Alegre','Vila Nair','Vila Ema','Campo Limpo','Catumbi','Parque Colonial','Vila Lageado','Parque da Mooca','Panamby','Parque Continental','Belenzinho','Chácara Mafalda','Jardim Consorcio','Jardim Sônia Regina','Jardim do Colegio','Sé','Jardim Peri','Vila Buarque','Vila Sao Paulo','Jardim Três Marias','Vila Socorro','Jardim Ipanema (Zona Oeste)','Casa Verde','Imirim','Vila Medeiros','Vila Gustavo','Jardim Esmeralda','Vila Constança','Santa Teresinha','Vila Dom Pedro II','Vila Isolina Mazzei','Vila Taquari','Vila Olimpia','Vila Cordeiro','Jardim Mália I','Penha de França','Vila São Paulo','Vila Penteado','Vila Bela','Jardim Europa','São Lucas','Vila Nhocune','Retiro Morumbi','Jardim Santo Amaro','Vila Inglesa','Vila Santa Catarina','Bom Retiro','Vila Almeida','Parque Savoy City','Vila Aurora','Sítio do Mandaqui','Vila Mazzei','Horto Florestal','Vila Santos','Vila Pompéia','Jardim Itapura','Parque Guarani','Jardim Itapeva','Água Rasa','Jardim Imperador (Zona Leste)','Jardim Maraba','São Miguel Paulista','Vila Aricanduva','Jardim Independencia','Vila Campo Grande','Lar São Paulo','Vila Pierina','Vila Santa Maria','Parada XV de Novembro','Vila Matilde','Vila Dionisia','Vila Carrao','Vila Mafra','Jardim Modelo','Santa Terezinha','Vila Centenário','Vila Oratório','Sítio Pinheirinho','Vila Noca','Vila Anastácio','Vila Espanhola','Jardim Santa Terezinha (Zona Leste)','Conjunto Residencial Jardim Canaa','Parque Taipas','Vila Pauliceia','Chácara Inglesa','Jardim Brasilia','Jardim Carombe','Loteamento City Jaragua','São Paul','Alto de Pinheiros','Piqueri','Vila Santo Estéfano','Vila Guarani','Vila Invernada','Usina Piratininga','Bela Aliança','City América','Vila Gertrudes','Nova Piraju','Rua Professor Cl','Jardim Avelino','Vila do Encontro','Itaquera','Vila Inah','Parque Anhembi','Jardim Norma','Vila Nova Cachoeirinha','Parque Edu Chaves','Jardim Anália Franco','Vila Costa Melo','Rua Enguaçú','Cursino','Jd Paulista','Jardim da Glória','Real Parque','Vila Dalva','Jardim Paulistano (Zona Norte)','Vila Gomes Cardim','Jardim Aricanduva','Vila Marieta','Freguesia do Ó','Alto da Mooca','Conjunto Habitacional Turistica','Vila Santa Edwiges','Jardim Brasil (Zona Sul)','Vila Anglo Brasileira','Pari','Vila Progredior','Vila Baruel','Parque Maria Luiza','Vila Anastacio','Vila Gumercindo','Vila Guarani (Zona Sul)','Vila Amélia','Vila Celeste','Jardim Campo Grande','Parque Boturussu','Vila Basileia','Vila Granada','Jardim Tremembe','Cidade Nova Heliópolis','Jardim Rosana','Jardim Primavera','Parque São Domingos','Vila Mangalot','Vila Irmãos Arnoni','Jardim Bélgica','Jardim Ivana','Vila Polopoli','Jardim Cordeiro','Jardim Bom Refúgio','Jardim Vazani','Vila dos Remedios','Cerq. Cesar','Cidade Líder','Jardim Regis','Rio Bonito','Quarta Parada','Vila Friburgo','Jardim Luanda','Cupecê','Parque São Lourenço','Vila Tramontano','Cidade Dutra','Vl Pompeia','Jardim Lallo','Pacaembu','Jardim Coimbra','Jardim Cidade Pirituba','Chácara Nossa Senhora do Bom Conselho','Vila União (Zona Leste)','Guarapiranga','Conjunto Habitacional Teotonio Vilela','Jardim Pirituba','Itaim Paulista','Raposo Tavares','Jardim Paqueta','Capela do Socorro','Cidade São Mateus','Jardim Monte Kemel','Jardim Novo Mundo','Jardim Satélite','Chácara Klabin','Vila Diva','Vila Independência','Jardim Santa Monica','Vila Bruna','Vila Francos','Vila Siqueira (Zona Norte)','Jardim Jaqueline','Vila Bancária Munhoz','Pirituba','Vila Barbosa','Brooklin Novo','Vila Silvia','Vila Chabilândia','Vila Curuçá Velha','Casa Verde Média','Parque Peruche','Vila Paiva','Vila Madalena','Jardim Sarah','Vila São Silvestre','Vila Lúcia','Jardim Pinheiros','Jardim Olympia','Jardim das Laranjeiras','Ferreira','São Judas','Vila Zelina','Jardim Maristela','Jaguaré','Vila Heliópolis','Jardim Iguatemi','Cidade Continental','Parque Sevilha','Vila Rui Barbosa','Jardim Alvina','Sítio da Figueira','Parada De Taipas','Jardim Sydney','Vila Pirituba','Jardim Sao Paulo(Zona Norte)','Jardim Vila Mariana','Parque São Rafael','Jardim Joao XXIII','Quinta da Paineira','Jardim Nice','Vila Moraes','Vila Guaca','Vila Paranaguá','Sítio Morro Grande','Jardim Daysy','Granja Julieta','Vila Paulistana','Moinho Velho','Jardim Paulistano','Vila Nelson','Vila Guilhermina','Jardim Caboré','Parque Imperial','Jardim Los Angeles','Jardim Cidália','Jardim Consórcio','Jardim Rosa Maria','Jardim Sul','Vila Esperanca','Vila Euthalia','Penha de Franca','Jardim Raposo Tavares','Mandaqui','Jardim Taboão','Vila Nossa Senhora do Retiro','Vila Nova Caledônia','Sete Praias','Vila Mirante','Morro Grande','Residencial Sol Nascente','Aeroporto','Cidade Ademar','Vila Sabrina','Jardim Artur Alvim','Terceira Divisão de Interlagos','Vila Albertina','Vila Gea','Vila Anhangüera','Parque Jabaquara','Parque dos Bancários','Jardim Itatinga','Vila Itaberaba','Chácara Seis de Outubro','Vila Monumento','Parque Paineiras','Siciliano','Vila Água Funda','Jardim Colonial','Agua Rasa','Parque da Vila Prudente','Vila Clarice','Jardim Vivan','Jardim Shangrila','Vila Nilo','Conjunto Residencial Vista Verde','Vila Marari','Jardim Santo André','Jardim Japao','Jardim Donaria','Vila Brasílio Machado','Vila Monte Alegre','Jardim Oriental','Vila Firmiano Pinto','Vila Anhanguera','Jardim Ondina','Vila Ida','Casa Verde Alta','Vila Amália (Zona Norte)','Vila Paulista','Vila da Saúde','Vila Re','Parque dos Príncipes','Vila Santa Virginia','Vila Jaguara','Vila Morumbi','Jardim Patente Novo','Vila Santa Teresa','Jardim Adutora','Jardim das Esmeraldas','Parque Panamericano','Jardim Joana DArc','Jardim Jussara','Jardim Colorado','Parque Santo Antônio','Bortolândia','Jardim Penha','Jardim Panorama','Jardim Piratininga','Vila Sônia','Jardim Líbano','Parque Nações Unidas','Jardim Palmares (Zona Sul)','Vila Maria Baixa','Vila Guarani (Z Sul)','Vila Sao Vicente','Vila Cláudia','Cangaiba','Jardim Iris','Vila Souza','Jardim Andaraí','Jardim do Lago','Jardim Amaralina','Vila Pita','Jardim do Tiro','Parque Santa Rita','Jardim das Flores','Vila Dalila','Cidade Vargas','Jardim Ipanema','Parque das Árvores','Jardim Maria Estela','Jardim dos Estados','Super Quadra','Vila Oratorio','Vila do Castelo','Maranhão','Vila Nova Manchester','Vila Macedópolis','Ponte Pequena','Cidade Patriarca','Jardim Everest','Veleiros','São Rafael','Vila Babilonia','Jardim Vitória Régia','Jardim São Paulo(Zona Norte)','Jardim das Pedras','Vila Primavera','Jardim Brasília (Zona Leste)','Chácara Flora','Jardim Morro Verde','Jardim Sapopemba','Vila dos Remédios','Jaragua','Vila Pereira Cerca','Vila Araguaia','Vila das Mercês','Jardim Rodolfo Pirani','Vila Canero','Chácara Monte Alegre','Jardim Marquesa','Vila Yolanda','Vila Antonio','Jardim São Bento','Vila Arriete','Jardim Boa Vista','Aricanduva','Vila Lais','Chácara Santa Etelvina','Serra da Cantareira','Santa Efigênia','Vl Argentina','Grajaú','Vila Zilda','Jardim Sao Bento','Vila Gouveia','Vila São José','Vila Olinda','Conjunto Residencial Jardim Canaã','Jardim Fonte do Morumbi','Jardim Maringá','Jardim Vitoria Regia','Vila Talarico','Vila Moreira','Jardim Guanca','Vila Roque','Vila Cisper','Vila Sao Francisco','Furnas','Vila Indiana','Jardim Cotinha','Cangaíba','Vila das Belezas','Jardim Sonia','Vila Império','Jardim Jabaquara','Jardim Nosso Lar','Jardim Paraíso','Jardim das Acacias','Parque Sao Rafael','Jardim Analia Franco','Luz','Instituto de Previdência','Paineiras do Morumbi','Vila Sonia','Burgo Paulista','Vila Azevedo','Vila Frugoli','Vila Romero','Vila Paulicéia','Chácara Gaivotas','Guapira','Vila Pedra Branca','Brasilândia','Pompeia','Parque América','Jardim Textil','Rolinópolis','Patriarca','Jardim Trussardi','Jardim São João (Jaraguá)','Jardim Ubirajara','Jardim Luzitânia','Jardim Ana Lúcia','Vila Bela Vista (Zona Norte)','Vila Rica','Jardim Novo Santo Amaro','Vila Castelo','Vila Cardoso Franco','Vila Conde do Pinhal','Perus','Vila Santa Isabel','Jardim Previdência','Vila Marina','Jardim Boa Vista (Zona Oeste)','Jardim Arize','Real Parque - Morumbi','Chácara Califórnia','Jardim Ideal','Vila Santo Antônio','Cidade Universitária','Parque Pereira','Jardim Labitary','José Bonifácio','Jardim Itapema','Vila Comercial','Engenheiro Goulart','Jardim Centenário','Jardim Guarau','Vila Ribeiro de Barros','Jardim Cláudia','Chácara Tatuapé','Parque Vitoria','Jardim Paris','Parque Sao Domingos','Jardim Sao Jorge','Jardim Campos','Jardim Regina','Conjunto Residencial Butanta','Chácara Itaim','Vila do Bosque','Vila Iório','Parque Anhangüera','Jardim Mariliza','Vila Miriam','Vila Jaragua','Jardim Matarazzo','Jardim Guairaca','Vila Pereira Barreto','Vila Tiradentes','Parque Cruzeiro do Sul','Vila Rio Branco','Jardim Novo Carrão','Jardim Egle','Jardim Ângela (Zona Leste)','Vila Cavaton','Jardim São Savério','Parque do Castelo','Vila Fiat Lux','Parque Alves de Lima','Núcleo do Engordador','Valo Velho','Alto do Pari','Vila Bonilha','Jardim Pedro José Nunes','Conjunto Habitacional Jova Rural','Vila Carmem','Vila Ivone','Conjunto Habitacional Padre Manoel da Nobrega','Vila Barreto','Super Quadra Morumbi','Jardim Mangalot','Jardim Nordeste','Jardim Franca','Vila Morse','Butanta','Parque dos Principes','Jardim São José (Zona Norte)','Jardim Alvorada','Conjunto Promorar Raposo Tavares','Sapopemba','Vila Santa Teresa (Zona Leste)','Jardim Nossa Senhora do Carmo','Parque Doroteia','Parque Maria Domitila','Jardim São Nicolau','Vila Carbone','Jardim Adelaide','Vila Zat','São João Clímaco','Vila Nova York','Vila Brasilândia','Jardim Morumbi','Vila Caraguatá','Nossa Senhora do Ó','Jardim Primavera (Zona Sul)','Vila Margarida','Vila Parque Jabaquara','Jardim Vitoria Regia (Zona Oeste)','Parque Císper','Canindé','Belém','Vila Sílvia','Vila Bonilha Nova','Vila Maria Luisa','Vila Santa Teresinha','Limoeiro','Jardim Danfer','Guaianases','Parque Esmeralda','Vila Cunha Bueno','Jardim Catanduva','Vila Princesa Isabel','Jardim Marabá','Cidade dos Bandeirantes','Parque Monteiro Soares','Vila California','Jaçanã','Vila Salete','Vila Giordano','Vila Fazzeoni','Vila Cruz das Almas','Jdm Maraba','Ingai','Vila Natalia','Vila Marte','Vila Buenos Aires','Parque Ipe','Jardim Sabará','Parque Cisper','Jardim Santa Lucrécia','Vila Siqueira','Altos de Vila Prudente','Jardim Francisco Mendes','Jardim Botucatu','Vila Jaguari','Parque Industrial Tomas Edson','Jardim Belém','Jardim Santa Maria','Brasili Ndia','Jardim Maria Rita','Chacara Nossa Senhora Aparecida','Vila Sao Luis','Praia Azul','Jardim Felicidade (Zona Oeste)','Vila Deodoro','Chácara Cruzeiro do Sul','Jardim Jua','Vila Sao Pedro','Vila Germinal','Jardim Cachoeira','Jardim Maria Luiza','Jardim Cristal','Núcleo Lageado','Vl. Pauliceia','Jardim Dona Sinhá','Conjunto Residencial Elisio Teixeira Leite','Vila Feliz','Jardim Triana','Parque Independência','Conjunto Residencial Prestes Maia','Jardim Selma','Vila Brasilina','Jardim Santa Cruz (Sacomã)','Jardim Miriam','Vila Antonina','Lapa de Baixo','Vila Arapuã','Jardim Sao Francisco','Jardim Martins Silva','Jardim Jaraguá','Vila Nova Alba','Rua Emílio Goel','Barro Branco','Vila Virginia','Vila Paranagua','Vila Car','Jardim Santa Helena','Vila Laís','Jardim Santo Antoninho','Jardim Independência','Capão Redondo','Jardim Panorama do Oeste','Vila das Merces','São João Climaco','Jardim Sao Saverio','Jardim das Camélias','Vila Carolina','Jardim São Paulo(Zona Leste)','Cidade Tiradentes','Vila Babilônia','São Mateus','Cidade Domitila','Vila Maracanã','Vila Imperio','Jardim Ipanema (Zona Sul)','Vila Damaceno','Vila Renato','Parque das Arvores','Conjunto Habitacional Instituto Adventista','Jardim Mitsutani','Jardim Patente','Ch Encosto','Jardim Eledy','Jardim Imperador','Jardim Santa Terezinha','Jardim Maria Virginia','Vila Nova Caledonia','Jardim Arpoador Zona Oeste','Balneário São Francisco','Jardim Vaz de Lima','City America','Ermelino Matarazzo','Vila Sao Silvestre (Zona Leste)','Jardim Mutinga','Jardim São Luis','Parque Rebouças','Chacara Santa Maria','Jardim Maria Duarte','Parque Regina','Jardim Sao Luiz','Jardim Wanda','Jardim Sandra','Chacara Nossa Senhora do Bom Conselho','Parque Maria Helena','Jardim Leônidas Moreira I','Jardim Imbé','Vila Erna','Jardim Brasília','Morro dos Ingleses','Jardim Palmares','VL Baruel','Pq. Maria Helena','Jardim da Campina','Vila Maracana','Jardim Santa Teresa','Vila Pirajussara','Jardim Lidia','NA','Jardim Ampliacao','Jardim Laura','City Jaragua','Jardim Lídia','Vila Santa Terezinha (Zona Norte)','Jardim Ponte Rasa','Jardim Lisboa','Vl Mascote','Conjunto Residencial Ingai','Vila Constanca','Jardim dos Manacas','Jardim Mascote','Jardim Cidalia','Jardim Soraia','Jardim Juá','Chácara Jaraguá','Vila Santo Estevão','Jardim Hercilia','Jardim Helena','Jardim Peri Peri','Praça da Árvore','Jardim Viana','Jd da Saúde','Jardim Dracena','Vila dos Andradas','Jardim Panorama (Zona Leste)','Jardim Petrópolis','Rua José Laborim','Rua Gregório Allegri','Jardim Thomaz','Chácara Nossa Senhora do Bom Conselho ','Vila Olympia','Jardim Rio Pequeno','Jardim Avenida','Vera Cruz','Vila Hebe','Vila da Paz','Jardim Hipico','Jardim Iae','Colonia - Zona Leste','Jardim Pereira Leite','Vila Mira','Jardim São Carlos (Zona Leste)','Jardim Felicidade (Zona Norte)','Parque Ibirapuera','Jardim Alzira','Jardim Germania','Jardim Maracá','Vila Aimore','Parque Residencial Julia','Vila Nova Carolina','Jardim Vista Linda','Vila Fachini','Cidade A E Carvalho','Jardim Capelinha','Jardim Porteira Grande','Jardim Marilu','Jardim Alfredo','Vila Progresso','Vila Alzira','Jd Marajoara','Jardim Fernandes','Horto do Ipê','Parque Santa Madalena','Rua José dos Reis','Parque Residencial da Lapa','Jardim Elba','Parque do Carmo','Vila Baby','Jardim Helga','Villaggio Panamby','Parque Palmas do Tremembé','Vila Tolstoi','Vila Carlos de Campos','Jardim Leonidas Moreira','Vila Romano','Jardim Jaragua','Vila Hamburguesa','Jardim Marcel','Conjunto Residencial Novo Pacaembu','Parque Sao Luis','Jardim das Perdizes','Jardim Santa Mônica','Jardim São Jorge (Raposo Tavares)','Jardim Libano','Jardim das Rosas (Zona Leste I)','Jardim São Gilberto','Vila Bela Vista','Rua Caraíbas','Vila Rosa','Vila Independencia','Chácara Santo Antônio Zona Leste','Vila Universitária','Jardim das Palmas','Vila Carioca','Jardim Cambara','Vila São Francisco (Zona Sul)','Jardim Vera Cruz','Vila Renato (Zona Norte)','Ibirapuera','Jardim DAbril','Boaçava','Jardim Edith','Vila Borges','Lajeado','Rua Luís da Silva Araújo','Vl R Feijo','Jardim Santa Efigenia','Jardim Mirante','Vila Santo Estefano','Vila Helena','Jardim Arpoador','Jardim Olinda','Vila São José‎','Jardim','Vila Diva (Zona Leste)','Balneário São José','Vila Natália','Vila rica','Vila Campanela','Jardim Mália II','Jardim Hebrom','Jardim Piqueroby','Umarizal','São Domingos','Rua Deputado Laércio Corte','Residencial Morumbi','Jardim Taboao','Jardim Sílvia (Zona Oeste)','Vila Missionária','Rua José Gonçalves','Rua Comandante Garcia DÁvila','Jardim Silvia(Zona Oeste)','Tatupé','Jardim Carlu','Jardim Panorama Doeste','Vila São Geraldo','Jardim Nélia','Jardim São Januário','Vila Aurea','Vila São Nicolau','Conjunto Residencial Butantã','Jardim Fonte do Morumbi ','Jardim Alto Pedroso','Cidade Antônio Estevão de Carvalho','Vila Central','Vila Nova Savoia','Jardim América da Penha','Parque Santa Amélia','Vila Santo Henrique','Jardim Sao Jose','Vila Natal','Jardim Angela (Zona Leste)','Vila São Silvestre (Zona Leste)','Rua Américo Brasiliense','Jardim Vale das Virtudes','Jardim Cruzeiro','Jardim Nova Germania','Jardim São Luís (Zona Sul)','Vila Lisboa','Parque Grajau','Vl. Iza','Rua São Serafim','Conjunto Residencial Salvador Tolezani','Jardim Sertaozinho','Jardim Guapira','Vila Divina Pastora','Rua José Maria Lisboa','Recanto Verde do Sol','Jardim D Abril','Jardim Itapemirim','Jard. Paulista','Vila Domitila','Jardim Ana Maria','Jardim Vergueiro (Sacomã)','Jardim Independencia','Parque Boa Esperança','Parque Guarapiranga','Alameda Jaú','Rua Barão do Triu','Vila Albano','Vila Ponte Rasa','Cidade Nova São Miguel','Colônia (Zona Leste)','Jardim São Cristóvão','Conjunto Residencial Sitio Oratório','Jardim Previdencia','Avenida Satélite','Vila Ester','Pirajussara','Parque Bairro Morumbi','Jardim Vila Carrão','Jardim Santa Adélia','Indo Paulo','Jardim Morumby','Jardim Promissão','Vila Industrial','V Campos Salles','204','BROOKLIN','Fazenda da Juta','Vila Mesquita','Jardim Vera Cruz(Zona Leste)','Jardim Prainha','Portal do Morumbi','Vila Brasilio Machado','Rua Barão do Tr','Pq. Savoy City','Conjunto Habitacional Santa Etelvina II','Avenida Chibarás','Jardim Planalto','Jardim de Lorenzo','Parque Real','Vila Londrina','Jardim Novo Taboão','Avenida Ibijaú','Jardim Nadir','Vl M Velho','Rua Doutor Laerte Setúbal','Rua Sansão Alves dos Santos','Recanto Paraíso','Rua Percílio Neto','Jardim Santa Adelia','Brooklyn','Jardim Mimar','Jardim Cotiana','Vila Bandeirantes','Parelheiros','Conjunto Habitacional Marechal Mascarenhas de Morais','Vila Sapopemba','Vila Elze','Jardim João XXIII','Jardim São Roberto','Rua Vigário Albernaz','Real Park','Cidade Satelite Santa Barbara','Vila Heliopolis','Jd S Roberto','Rua José Batista Pereira','Jardim Sao Roberto','V Morumbi','Vila Guedes','Rua Canário','Boenida Indianó','Aosque da Saúde','São Pa','Jardim Jaçanã','Indianópo','Vila Nova Utinga','vila prudente','Vl Firmiano','Alameda dos Guat','Parque Residencial Oratorio','Jardim Tiete','Jardim Grimaldi','Parque Sao Lucas','Rua Antônio Carlos da Fonseca','Parque Planalto','Iguatemi','Jardim São Francisco (Zona Leste)','Jardim Jamaica','Rua Flórida','Avenida dos Carinás','Rua Édison','Conjunto Promorar Sapopemba','Vila Ivg','Vila Nova Pauliceia','Jardim Aurelia','Avenida Aratãs','Vila Monte Santo','Rua César Pina','Rua Marquês Olinda','Jardim Ibitirama','Jardim Campo Limpo','Jardim Jaú (Zona Leste)','Vila Teresinha','Saúde/Vila Mariana','Vila Santa Ines','Vila Campo Belo','Vila Arapua','Água Funda','Ch. Santo Antônio','Chac. St Antônio','Chac. Santo Anton','Rua Panônia','Recanto Morumbi','Fazenda Aricanduva','Capital','Vila Adalgisa','Cerqueira Cezar','Vila Claudia','Vila Fernandes','Rua Mário Amaral','Rua Cândida Medeiros da Silva','Instituto de Previdencia','Vila Libanesa','Jardim Adhemar de Barros','Jard Paulista','Jardim Rizzo','Jardim Record','Vila Sao Luis(Zona Oeste)','Vila São Luís(Zona Oeste)','Adalgisa','Rua Vitoantônio Del Vecchio','Vila Caraguata','Conjunto Habitacional Juscelino Kubitschek','Jardim Nossa Senhora Aparecida','Jardim Santos Dumont','Jardim Cotching','Parque Savoi City','Rua do Lavapés','Vila Dinorah','Jd América','Jardim Eliane','Jardim Têxtil','Jd S Teresinha','São Pau','Jardim Santa Terezinha (Zona L','Jardim da Gloria','Guaianazes','Jardim Odete','Rua Abílio Soares','Parque Santo Eduardo','Conjunto Habitacional Fazenda do Carmo','C Cesar','Rua Inácio Pereira d','Rua Hemisfério','Jardim Brasilia (Zona Leste)','Água Ralo','Jardim Maringa','Vila Universitaria','Jardim Tango','Jardim Imperial','Para Pau','Conjunto Habitacional Inácio Monteiro','[no name]','Vila Chuca','Jardim Ipanema (Zona Leste)','Rua Maranhão','Vl Madalena','Vila Caulo','Conjunto Habitacional Padre José de Anchieta','Jardim Universidade Pinheiros','Chácara Sto Antônio','Conjunto Residencial Jose Bonifacio','Jardim Dabril','Jardim Dinorah','Morada do Sol','Jardim Bela Vista','Jd Analia Franco','Jardim Caguassu','Jardim Novo Carrao','Vila Sao Domingos','Jardim Pedra Branca','Jardim Ester Yoland','Jd D Abril','Fazenda Caguaçu','Cerqueiral Teles','Vila Lúcia Elvira','Rua Ferreira de Araújo','Rua Doutor Hélio Fidelis','Jardim AM Rica','Rua Anália Franco','Jardim São Pedro','Jardim São José (Artur Alvim)','Parque Artur Alvim','Higienólo','Cidade Centenário','Rua do Paraíso','V Mariana','Rua Inácio Manuel Álvares','CerqMarquês de','Colônia','Jardim São Remo','Rua Cândido Lac','Vila Popular','Rua Anália Fran','Chacara Santo Antonio (Zona Le','Conjunto Habitacional Padre Manoel da Nóbrega','Jardim Bonifacio','Gamelinha','Bixiga','Rua Caçaquera','Vila Zefira','Vila Bertioga - Mooca','Vila Cosmopolita','Rua Itambé','Jdim América','Consola�ca','Vila Jatai','Jardim Marília','Jardim do Divino','Rua Cuiabá','Vila Santa Cruz (Zona Leste)','Praça General Porto Carreiro','Santa Ifigênia','Rua Cayowaá','Conjunto Habitacional Padre Manoel de Paiva','Sumar�a','Rua Antúrios','Rua Ourânia','São Pau�ão','Lageado','Cidade Antonio Estevão de Carvalho','Jardim República','C. P. Man. de Paiva','Vila Argentina','Jd Aricanduva','Rua Luís Coelho','Jardim Lajeado','Rua São Vicente de Paulo','Vila Ca','A. Pinheiros','Bresser','Santa Cecíl','V Pompeia','Guaiaúna','Parque da Lapa','Rua Apinajés','Vila Nancy','Jardim Lourdes','Jardim Liderança','São Paupolis','Jardim Jacarandas','Rua Piauí','Rua Serra de Bragança','Vila Graziela','Vila Santa Cruz','Rua Leão Coroad','Vl Bertioga','Jd São Francisco','Chac Paraíso','Higianopolis','Cohab José Bonifaci','Tatuapépolis','Avenida Marechal M�','City Boacava','Jardim do Campo','Rua Cândido Lacerd','Jardim Soares','Cerquda Otacíli','Jardim Ipanema(Zona Leste)','Parque das Flores','Avenida Higienópol','Vila Santa Izabel','Cidade','Perqueira César','Vila Arisi','176','Se','São Miguel','Jardim Monjolo','Vila Picinin','Jardim Verônia','Vila Zulmira','Vila Iorio','Vila Boaçava','Jardim Rossin','Itaberaba','Jardim do Colégio (Zona Norte)','Cachoeirinha','Vila Hermínia','Vila Portuguesa','Vila Jaraguá','Vila Conceição','Vila Brasil','Jardim Marisa','Vila Vitório Mazzei','Jardim Centenario','Vila Yara','Jardim Santa Inês','Barro Branco (Zona Norte)','Cidade D Abril','Parque Ramos Freitas','Jardim Cecy','Vila Amalia (Zona Norte)','Jardim Antártica','Vila Amália','Jardim Ataliba Leonel','Jardim Ibiratiba','Vila Dorna','Jardim Guarani','Jardim Britânia','Jardim dos Francos','Rua Doutor Luís Barreto Filho','Vila Irmaos Arnoni','Cohab Taipas','Ponte Rasa','Parque Penha','Jardim Tua','Vila Siria','Vila Jacuí','Jardim Camargo Novo','Nossa Senhora do Ö','Jardim Gonzaga','Chácara São João','Vila Robertina','Vila Bianca','Vila Rosaria','Sítio do Morro','Vila América','Rua Tomé Braga','Vila Americana','Conjunto Residencial Santa Terezinha','Rua Barão de São Luís','Parque Anhanguera','Jardim Jaraguá (São Domingos)','Jardim Brasil','Chácara Nossa Senhora Aparecida','City Pinheirinho','Industrial Anhangüera','Jardim Sao Roque','Parque Itaberaba','Jardim Almanara','Vila Serralheiro','Jardim Santa Ines','Vila Piauí','Vila Aparecida','Vila Norma','Rua Padre João Gua','Vila São Vicente','Vila America','Cidade Nitro Operária','Jardim São Luís (Zona Leste)','Jardim Santo Elias (São Miguel)','Frguesia do o','Pq. do Mandaqui','Vila Ramos','Vila Maria Trindade','Jardim Romano','Parque Guaianazes','Jardim Joamar','Parque Palmas do Tremembe','Avenida Luís Stamatis','Parque Paulistano','Jardim das Oliveiras','Jardim Sao Jose (Zona Norte)','Chacara Do Encosto','Cidade Nitro Química','Vila Nina','Vl Amélia','Vila Continental','Cj Res Sto Antônio','Parque Tiete','Vila Joao Batista','Jardim Bibi','Jardim Virgínia Bianca','Jardim Santa Cruz (Zona Norte)','Jardim Estrela Dalva','Vila Perus','Jardim Vista Alegre','Vila Fanton','Vila Homero','Jardim Santo Onofre','Jardim São Ricardo','Santa Therezinha','Jardim Julieta','Conjunto Habitacional Vila Nova Cachoeirinha','Jardim Celia','Rua Antônio Ca','Jardim França','Vila Progresso (Zona Norte)','Jardim Antartica','Jardim São Carlos','Vila Nova Curuçá','Vila Santa Lúcia','Vila Curuçá','Jardim Sao Vicente','Jardim Silva Teles','Pq. São Domingos','Vila Santa Inês','Parque Anhangüera (São Domingos)','Vila Genioli','Vila Bancaria Munhoz','Conjunto Habitacional Turística','Jardim Casa Pintada','Jardim Sao Sebastiao','Vila Piaui','Vila Arcadia','Vila Paulistania','Vila União','Vila Uniao(Zona Norte)','Vila Diva (Zona Norte)','Jardim Sao Francisco (Zona Leste)','Rua Jacaré-Copaíba','Jardim Irene','Jardim Etelvina','Alto Mandaqui','Jardim do Colegio (Zona Norte)','Vila Vitorio Mazzei','Jardim Elisa Maria','Estância Jaraguá','Jardim Flor de Maio','Jardim Lider','Anhanguera','Casa Verde Baixa','Jaguará','Jardim Castelo','Vl Paranagua','Avenida São Miguel','Vila Izolina','Jardim São Miguel','Vila dos Andrades','Rua Maria Cândida','Jardim para','Vila Verde','Jardim Santo Antônio','Jardim Laone','Jardim das Camelias','Vila Jacui','Rua dos Maracujás','Cidade São Miguel','Vila Portugal','Jd São Paulo','Vila Boacava','Jardim Maracanã','Jardim Picolo','Jardim Tiro Ao Pombo','Jardim Elisio','Vila Sao Geraldo','Jardim São Sebastião','Rua Engenheiro César','Jardim Belem','Parque São Luis','Vila Cachoeira','Chácara Santana','Rua Paulo Gonçalves','Vila Nova Jaraguá','Jardim Célia','Jardim Paraiso','Taipas','Jardim Yara','Parada','Jardim São Vicente','Vila Santista','Serra Da Cantareira','Jardim Monte Alegr','Jd Santa Ines','City Recanto Anastácio','Jardim das Graças','Vila Acre','Jardim Maracana','Vila Lucia','Vl. Nova Conceic','Vila Cleonice','Vila Macedopolis','Jardim Rubio','Itaim','Vila Nov�nio Pereira do Rio','Chácara Klabim','Alto Klabin','Vila Bancária','Conjunto Habitacional Barreira Grande','Jardim Teresa','Vila Bancaria','Vila Novonções','Jardim São João (São Rafael)','Jd Vila Mariana','Rua Montesquiéu','Jardim Iva','Jardim Gilda Maria','Vila Oaulo','Parque Independencia','Jardim Luzitania','Vl. Prudente','V Clementino','Vl Mariana','Institova Conceição','Klabin','V N Conceição','Jd Independ.','Km 21 da Raposo','Jardim Claudia','Rua João Luís Vives','Jd Europa','Jd Bonfiglioli','Conjunto Habitacional Castro Alves','Vila Sao Jose','Vila Olulo','Jardim Itápolis','Rua Fidêncio Ramos','Jardim Cinco de Julho','Vila Funchal','Jd Guedala','Rua Báltico','Rua Luís Dib Zogaib','Gleba do Pêssego','Vila Marilena','Jardim Batalha','Jardim São José','itaim','Vila Miami','Vila Anadir','Jardim Aurélia','Vila Olío','Vila Darli','Jardim Lucia','Rua Gonçalo Marinho de Castro','Jardim Luísa','Rua Inhambú','Chácara Kablin','Jardim Arpoardor','Vl. Mariana','Vila Guarani(Zona Leste)','Jardim São José (São Mateus)','Vila Alois','Tato Pau','Jdm Lucia','Jardim Peri-Peri','Jardim Augusto','Rua Barão de Tramandaí','Jardim Nova Vitória II','VILA PRUDENTE','Avetio da Figueira','Jardim Panorama DOeste','Jardim Paraguacu','Vila Fátima','Vão Paulo','Parque dos Bancarios','Vila Nova','Jardim da Laranjeira (Zona Leste)','Parque Sonia','Rua Vinte e Três de','Sao Judas','Jd IV Centenário','Avenida República do Líbano','Educandário','Jardim Nelly','Jardim das Rosas (Zona Leste)','Jardim Ibirapuera','Vila Sirene','Jardim São Jorge','Vl Monumento/Ipiran','Rua São Pompônio','Vila Arcádia','Jardim Miragaia','Erm Matarazzo','Rua Tapiraí','Vila Nova Teresa','Vila Itaim','Vila Brasilandia','Jardim Margarida','Vila Duarte','PENHA','Jardim Sao Ricardo','São Pauanca','Vila Bauab','Avenida Santa Inês','Rua Luís Antônio dos Santos','Rua Isaías Malentec','VL Ester','Vila Pedroso','Vila Raquel','Rua Pianú','Consolarrão','Santa Cecelia','Vila Corberi','Rua Suécia','Jardim Sao Jose (Artur Alvim)','Rua Iná','Jardim Thealia','Jardim Helian','I Bibi','Cohab Juscelino','Rua da Consolação','Jardim Santa Cruz (Sacoma)','Jardim Itacolomi','Jardim Petropolis','Jardim Santo Andre','Brooklin Velho','Jardim Seckler','Vila Sao Francisco (Zona Sul)','Conjunto Residencial Sitio Oratorio','Chc. Sto Antônio','Vl. Monte Alegre','Rua Antônio Portugal','Cerqueirímbolo','Vila dos Minérios','Jardim Sao Jorge (Raposo Tavares)','Jardim Guaraú','Jardim Valparaiso','Cidade DAbril','Jardim Anhangüera','Conjunto Habitacional Brigadeiro Eduardo Gomes','Portal dos Bandeirantes','Jardim Damasceno','Jardim Russo','Jardim Adelfiore','Jardim Fontalis','Vila Sulina','Jardim Carombé','Vila Dona Augusta','Jardim Uniserve','Jardim Brasília (Zona Norte)','Vila Caiúba','Jardim Santa Fé (Zona Oeste)','Jardim dos Ipês','Jardim Guança','Vila Amelia','Jardim Veronica','TremePaul','Jardim Taipas','Vila Lourdes','Jardim Tremembé','Sítio do Piqueri','Jardim Rincão','Conjunto City Jaraguá','Chácara Três Meninas','Jardim Bandeirantes','Vl. Mazzei','Vila Ana Rosa','Jardim São João (Zona Norte)','Jardim Bandeirantes (Zona Norte)','São Paundia','Sítio Barrocada','Jardim Monte Belo','Jardim Recanto Verde','Jardim Filhos da Terra','Conjunto City Jaragua','Santa Ines','Vila Clara','Jardim Neila','Freguesia do O','Jardim Britania','Vila Caiuba','Conjunto Residencial Elísio Teixeira Leite','Jardim Sao Joao (Jaragua)','VL Bandeirantes','Vila Silva Teles','Jardim Felicidade','Jardim Primavera (Zona Norte)','Vila Aimoré','Jardim do Colégio','Jardim Monte Alegre (Zona Norte)','Jardim Paquetá (Zona Norte)','Jardim Santa Lucrecia','Vila Doutor Eiras','Jardim Maria Eugênia','Vila Ismenia','Parque Mandi','Vila Piracicaba','Jardim Santo Alberto','Vila Fidalgo','Jardim São Luís (Zona Norte)','Chácara Figueira Grande','Rua Francisca Júlia','Jardim Maggi','Rua Motan','Jardim Princesa','Parada de Taipas','Vila Chica Luisa','Protendit','Vila Nova Jaragua','Jardim Shangrilá (Zona Norte)','Chácara Maria Trindade','Jardim Cabucu','Vila João Batista','Conjunto Residencial Bandeirantes','Coronel Sezefredo Fagundes','Rua André Chenier','Jardim Brasilia (Zona Norte)','Jardim Itália','Sano Paulo','CháDoutor Cândido','Jardim Aurora','Jardim Lageado','São Paecília','Guaiauna','Vila Nova Jaguare','Consola�lo','Rua da G','Vila Nova Jaguaré','Sumar','Vila Lucia Elvira','Rua Alves Guimarães','Cidade São Fran','Centro - São Paulo']
tipos_imovel_lista = ['Casa','Comercial','Apartamento','Flat','Condomínio','Depósito','Loteamento Residencial','Cobertura','Loja','Prédio Residencial','Escritório','Loteamento Comercial','Kitnet','Prédio Comercial','Clínica','Casa de Campo','Fazenda']
# Cria os campos de entrada para as features
bairro = st.selectbox('Bairro', bairros_lista)
tipo_imovel = st.selectbox('Tipo de Imóvel', tipos_imovel_lista)
quartos = st.number_input('Número de Quartos', min_value=0, value=2)
banheiros = st.number_input('Número de Banheiros', min_value=0, value=2)
vagas = st.number_input('Número de Vagas na Garagem', min_value=0, value=1)
area_util = st.number_input('Área Útil (m²)', min_value=0, value=50)

bairro = pd.Dataframe([bairro]).astype('category')
tipo_imovel = pd.Dataframe([tipo_imovel].astype('category')

# Cria um botão para realizar a predição
if st.button('Prever Preço'):
    # Cria um DataFrame com os valores de entrada
    input_data = pd.DataFrame({
        'bairro': [bairro],
        'tipo_imovel': [tipo_imovel],
        'quartos': [quartos],
        'banheiros': [banheiros],
        'vagas_garagem': [vagas],
        'area_util': [area_util]
    })

    # Faz a predição usando o modelo carregado
    try:
        prediction = model.predict(input_data)[0]
        st.success(f'Preço de venda estimado: R$ {prediction:.2f}')
    except ValueError as e:
        st.error(f"Erro ao realizar a predição: {e}. Verifique os valores inseridos.")
