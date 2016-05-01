# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from contextlib import closing

from django.core.management.base import BaseCommand
from django.db import connection

from politicians.models import (
    PoliticalParty, Institution, PoliticalOffice, Politician,
    Mandate, Ethnicity, Education, PoliticianAlternativeName,
    PoliticianEventType, PoliticianEvent, PoliticianPoliticalParty,
    Candidacy, Election, CandidacyStatus, City, State, Country,
    MaritalStatus, Nationality, Occupation
)


columns_2014 = [
    'DATA_GERACAO',
    'HORA_GERACAO',
    'ANO_ELEICAO',
    'NUM_TURNO',
    'DESCRICAO_ELEICAO',
    'SIGLA_UF',
    'SIGLA_UE',
    'DESCRICAO_UE',
    'CODIGO_CARGO',
    'DESCRICAO_CARGO',
    'NOME_CANDIDATO',
    'SEQUENCIAL_CANDIDATO',
    'NUMERO_CANDIDATO',
    'CPF_CANDIDATO',
    'NOME_URNA_CANDIDATO',
    'COD_SITUACAO_CANDIDATURA',
    'DES_SITUACAO_CANDIDATURA',
    'NUMERO_PARTIDO',
    'SIGLA_PARTIDO',
    'NOME_PARTIDO',
    'CODIGO_LEGENDA',
    'SIGLA_LEGENDA',
    'COMPOSICAO_LEGENDA',
    'NOME_LEGENDA',
    'CODIGO_OCUPACAO',
    'DESCRICAO_OCUPACAO',
    'DATA_NASCIMENTO',
    'NUM_TITULO_ELEITORAL_CANDIDATO',
    'IDADE_DATA_ELEICAO',
    'CODIGO_SEXO',
    'DESCRICAO_SEXO',
    'COD_GRAU_INSTRUCAO',
    'DESCRICAO_GRAU_INSTRUCAO',
    'CODIGO_ESTADO_CIVIL',
    'DESCRICAO_ESTADO_CIVIL',
    'CODIGO_COR_RACA',
    'DESCRICAO_COR_RACA',
    'CODIGO_NACIONALIDADE',
    'DESCRICAO_NACIONALIDADE',
    'SIGLA_UF_NASCIMENTO',
    'CODIGO_MUNICIPIO_NASCIMENTO',
    'NOME_MUNICIPIO_NASCIMENTO',
    'DESPESA_MAX_CAMPANHA',
    'COD_SIT_TOT_TURNO',
    'DESC_SIT_TOT_TURNO',
    'EMAIL',
]

columns_2010 = [
    'DATA_GERACAO',
    'HORA_GERACAO',
    'ANO_ELEICAO',
    'NUM_TURNO',
    'DESCRICAO_ELEICAO',
    'SIGLA_UF',
    'SIGLA_UE',
    'DESCRICAO_UE',
    'CODIGO_CARGO',
    'DESCRICAO_CARGO',
    'NOME_CANDIDATO',
    'SEQUENCIAL_CANDIDATO',
    'NUMERO_CANDIDATO',
    'CPF_CANDIDATO',
    'NOME_URNA_CANDIDATO',
    'COD_SITUACAO_CANDIDATURA',
    'DES_SITUACAO_CANDIDATURA',
    'NUMERO_PARTIDO',
    'SIGLA_PARTIDO',
    'NOME_PARTIDO',
    'CODIGO_LEGENDA',
    'SIGLA_LEGENDA',
    'COMPOSICAO_LEGENDA',
    'NOME_LEGENDA',
    'CODIGO_OCUPACAO',
    'DESCRICAO_OCUPACAO',
    'DATA_NASCIMENTO',
    'NUM_TITULO_ELEITORAL_CANDIDATO',
    'IDADE_DATA_ELEICAO',
    'CODIGO_SEXO',
    'DESCRICAO_SEXO',
    'COD_GRAU_INSTRUCAO',
    'DESCRICAO_GRAU_INSTRUCAO',
    'CODIGO_ESTADO_CIVIL',
    'DESCRICAO_ESTADO_CIVIL',
    'CODIGO_NACIONALIDADE',
    'DESCRICAO_NACIONALIDADE',
    'SIGLA_UF_NASCIMENTO',
    'CODIGO_MUNICIPIO_NASCIMENTO',
    'NOME_MUNICIPIO_NASCIMENTO',
    'DESPESA_MAX_CAMPANHA',
    'COD_SIT_TOT_TURNO',
    'DESC_SIT_TOT_TURNO',
]

columns_2012 = list(columns_2010)
columns_2012.append('EMAIL')


class Command(BaseCommand):

    def create_to_date_function(self):
        print 'Creating to_date function'
        with closing(connection.cursor()) as cursor:
            cursor.execute('''
                CREATE OR REPLACE FUNCTION public.my_to_date (
                    s_text VARCHAR, s_mask VARCHAR
                )
                RETURNS date AS
                    $body$
                    DECLARE
                        l_date date;
                    BEGIN
                        l_date := to_date(s_text, s_mask);
                        RETURN l_date;
                    EXCEPTION
                        WHEN others THEN
                        RETURN null;
                    END;
                    $body$
                LANGUAGE 'plpgsql'
                VOLATILE
                CALLED ON NULL INPUT
                SECURITY DEFINER
                COST 100;
        ''')

    def convert_file(self, source, target):
        # iconv -f latin1 -t utf-8 consulta_cand_2012_SP.txt > blah.txt
        source_encoding = 'iso-8859-1'
        target_encoding = 'utf-8'
        source = open(source)
        target = open(target, 'w')
        target.write(
            unicode(source.read(), source_encoding).encode(target_encoding)
        )

    def create_tse_table(self):
        with closing(connection.cursor()) as cursor:
            try:
                cursor.execute('DROP TABLE tse_csv2')
            except:
                pass
            cursor.execute('''
                CREATE TABLE tse_csv2(
                    id serial NOT NULL,
                    DATA_GERACAO varchar(10),
                    HORA_GERACAO time,
                    ANO_ELEICAO int,
                    NUM_TURNO int,
                    DESCRICAO_ELEICAO varchar(255),
                    SIGLA_UF varchar(2),
                    SIGLA_UE varchar(100),
                    DESCRICAO_UE varchar(255),
                    CODIGO_CARGO int,
                    DESCRICAO_CARGO varchar(255),
                    NOME_CANDIDATO varchar(255),
                    SEQUENCIAL_CANDIDATO varchar(255),
                    NUMERO_CANDIDATO int,
                    CPF_CANDIDATO varchar(11),
                    NOME_URNA_CANDIDATO varchar(255),
                    COD_SITUACAO_CANDIDATURA int,
                    DES_SITUACAO_CANDIDATURA varchar(255),
                    NUMERO_PARTIDO int,
                    SIGLA_PARTIDO varchar(10),
                    NOME_PARTIDO varchar(255),
                    CODIGO_LEGENDA varchar(255),
                    SIGLA_LEGENDA varchar(255),
                    COMPOSICAO_LEGENDA varchar(255),
                    NOME_LEGENDA varchar(255),
                    CODIGO_OCUPACAO int,
                    DESCRICAO_OCUPACAO varchar(255),
                    DATA_NASCIMENTO varchar(10),
                    NUM_TITULO_ELEITORAL_CANDIDATO varchar(100),
                    IDADE_DATA_ELEICAO int,
                    CODIGO_SEXO int,
                    DESCRICAO_SEXO varchar(30),
                    COD_GRAU_INSTRUCAO int,
                    DESCRICAO_GRAU_INSTRUCAO varchar(255),
                    CODIGO_ESTADO_CIVIL int,
                    DESCRICAO_ESTADO_CIVIL varchar(255),
                    CODIGO_COR_RACA int,
                    DESCRICAO_COR_RACA varchar(255),
                    CODIGO_NACIONALIDADE int,
                    DESCRICAO_NACIONALIDADE varchar(255),
                    SIGLA_UF_NASCIMENTO varchar(2),
                    CODIGO_MUNICIPIO_NASCIMENTO int,
                    NOME_MUNICIPIO_NASCIMENTO varchar(255),
                    DESPESA_MAX_CAMPANHA real,
                    COD_SIT_TOT_TURNO int,
                    DESC_SIT_TOT_TURNO varchar(255),
                    EMAIL varchar(255)
                );'''
            )
            # print 'psql politicos -U postgres -c "\copy tse_csv2({0}) FROM ~/Desktop/blah.txt DELIMITER \';\' CSV;"'.format(', '.join(data))

    def handle(self, *args, **kwargs):
        with closing(connection.cursor()) as cursor:
            cursor.execute('''
                SET LOCAL temp_buffers="256MB";
                SET LOCAL maintenance_work_mem="128MB";
            ''')

        # self.create_tse_table()
        # self.import_tse_data()
        # self.create_indexes()
        # self.create_to_date_function()
        self.insert_data()

    def import_tse_data(self):
        elections = Election.objects.all()
        for election in elections:
            print 'Starting election {0}'.format(election)
            states = [(x.siglum, x.name) for x in State.objects.all()]
            states = ((u'BR', u'Brasil'),) + tuple(states)
            for state_siglum, state_name  in states:
                try:
                    print 'Starting state {0}'.format(state_siglum)
                    file_name = '/home/metal/Desktop/eleicoes/{0}/consulta_cand_{0}/consulta_cand_{0}_{1}.txt'.format(election.year, state_siglum)
                    self.convert_file(file_name, '/home/metal/Desktop/blah.txt')
                    self.copy_data(election.year)
                except Exception as e:
                    print e

        """
        year = 2004
        state = 'MG'
        print 'Starting state {0}'.format(state)
        file_name = '/home/metal/Desktop/eleicoes/{0}/consulta_cand_{0}/consulta_cand_{0}_{1}.txt'.format(year, state)
        self.convert_file(file_name, '/home/metal/Desktop/blah.txt')
        self.copy_data(year)
        """

    def copy_data(self, year):
        if year == 2014:
            data = columns_2014
        elif year == 2012:
            data = columns_2012
        else:
            data = columns_2010

        with closing(connection.cursor()) as cursor:
            query = "COPY tse_csv2({0}) FROM '/home/metal/Desktop/blah.txt' WITH CSV DELIMITER ';';".format(', '.join(data))
            cursor.execute(query)
            cursor.execute('COMMIT;')

    def create_indexes(self):
        string_indexes = [
            'cpf_candidato', 'descricao_ocupacao', 'descricao_grau_instrucao',
            'sigla_uf', 'descricao_ue', 'descricao_estado_civil',
            'descricao_cor_raca', 'descricao_nacionalidade',
            'desc_sit_tot_turno', 'des_situacao_candidatura',
            'nome_urna_candidato',
        ]
        integer_indexes = ['codigo_ocupacao', 'codigo_sexo']

        print 'Creating indexes...'
        with closing(connection.cursor()) as cursor:
            for x in string_indexes:
                print '* {0}'.format(x)
                cursor.execute('CREATE INDEX CONCURRENTLY tse_{0}_idx ON tse_csv2 (LOWER({0}));'.format(x))
            for x in integer_indexes:
                print '* {0}'.format(x)
                cursor.execute('CREATE INDEX CONCURRENTLY tse_{0}_idx ON tse_csv2 ({0});'.format(x))

    def insert_data(self):
        with closing(connection.cursor()) as cursor:
            """
            # FIXME: slug
            # http://theoryapp.com/generate-slug-url-in-mysql/
            # https://gist.github.com/JotapePinheiro/2348335
            # http://scottbarnham.com/blog/2010/12/20/make-a-slug-in-postgresql-translating-diacritics/
            print 'Inserting occupations'
            cursor.execute('''
                INSERT INTO politicians_occupation(name)
                SELECT lower(descricao_ocupacao)
                FROM tse_csv2
                GROUP BY descricao_ocupacao
                ORDER BY descricao_ocupacao;
            ''')

            print 'Inserting alternative names'
            cursor.execute('''
                INSERT INTO politicians_politicianalternativename(name)
                SELECT lower(nome_urna_candidato)
                FROM tse_csv2
                GROUP BY nome_urna_candidato;
            ''')

            print 'Inserting educations'
            cursor.execute('''
                INSERT INTO politicians_education(name)
                SELECT lower(descricao_grau_instrucao)
                FROM tse_csv2
                GROUP BY descricao_grau_instrucao;
            ''')

            print 'Inserting candidacy status'
            cursor.execute('''
                INSERT INTO politicians_candidacystatus(name)
                SELECT lower(des_situacao_candidatura)
                FROM tse_csv2
                GROUP BY des_situacao_candidatura;
            ''')

            print 'Inserting marital status'
            cursor.execute('''
                INSERT INTO politicians_maritalstatus(name)
                SELECT lower(descricao_estado_civil)
                FROM tse_csv2
                GROUP BY descricao_estado_civil;
            ''')

            print 'Inserting nacionality'
            cursor.execute('''
                INSERT INTO politicians_nationality(name)
                SELECT lower(descricao_nacionalidade)
                FROM tse_csv2
                GROUP BY descricao_nacionalidade;
            ''')

            print 'Inserting Cities'
            cursor.execute('''
                INSERT INTO politicians_city(name, state_id)
                SELECT descricao_ue, (SELECT id FROM politicians_state ps WHERE ps.siglum = tc.sigla_uf) AS state_id
                FROM tse_csv2 tc
                WHERE tc.descricao_ue != \'BRASIL\'
                GROUP BY tc.descricao_ue, tc.sigla_uf;
            ''')
            """
            print 'Inserting politician'
            cursor.execute('''
                INSERT INTO politicians_politician(
                    name,
                    cpf,
                    gender,
                    place_of_birth,
                    date_of_birth,
                    ethnicity_id,
                    nationality_id,
                    state_id,
                    marital_status_id,
                    education_id,
                    email
                )
                SELECT
                    LOWER(tc.nome_candidato) AS name,
                    tc.cpf_candidato AS cpf,
                    CASE WHEN @tc.codigo_sexo = 2 THEN 'M' WHEN @tc.codigo_sexo = 4 THEN 'F' ELSE 'N' END AS gender,
                    LOWER(tc.nome_municipio_nascimento) AS place_of_birth,
                    my_to_date(tc.data_nascimento, 'DD/MM/YYYY') AS date_of_birth,
                    pet.id AS ethnicity_id,
                    nat.id AS nationality_id,
                    st.id AS state_id,
                    mt.id AS marital_status_id,
                    ped.id AS education_id,
                    LOWER(tc.email)
                FROM tse_csv2 tc
                    INNER JOIN (SELECT MIN(id) AS id, cpf_candidato FROM tse_csv2 GROUP BY cpf_candidato) tc2 ON tc2.id = tc.id
                    FULL OUTER JOIN politicians_nationality nat ON LOWER(nat.name) = LOWER(tc.descricao_nacionalidade)
                    FULL OUTER JOIN politicians_maritalstatus mt ON LOWER(mt.name) = LOWER(tc.descricao_estado_civil)
                    FULL OUTER JOIN politicians_state st ON st.siglum = tc.sigla_uf_nascimento
                    FULL OUTER JOIN politicians_ethnicity pet ON pet.name = INITCAP(tc.descricao_cor_raca)
                    FULL OUTER JOIN politicians_education ped ON LOWER(ped.name) = LOWER(tc.descricao_grau_instrucao)
                ORDER BY
                    tc.cpf_candidato DESC;
            ''')

            """
            print 'Inserting politician alternative names'
            cursor.execute('''
                INSERT INTO politicians_politician_alternative_names(
                    politician_id,
                    politicianalternativename_id
                )
                SELECT
                    (SELECT id FROM politicians_politician pp WHERE pp.cpf = tc.cpf_candidato AND pp.name = tc.nome_candidato) as politician_id,
                    (SELECT id FROM politicians_politicianalternativename pa WHERE pa.name = tc.nome_urna_candidato) as politicianalternativename_id,
                FROM tse_csv2 tc
            ''')
            """

            """
            # FIXME: slug;
            # already in commands
            print 'Inserting Ethnicity'
            cursor.execute('''
                INSERT INTO politicians_ethnicity(name)
                SELECT lower(descricao_cor_raca)
                FROM tse_csv2
                GROUP BY descricao_cor_raca;
            ''')
            """
