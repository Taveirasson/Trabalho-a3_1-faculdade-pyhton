mysql -u root -p

create database atividade;

use atividade;


create table usuario(
	id int(3) auto_increment,
	nome varchar(50) not null,
	email varchar(50) not null unique,
    data_nasc date,
    telefone varchar(20),
    apelido varchar(50) not null unique,
    senha varchar(100) not null,
    primary key (id)
);

insert into usuario (nome, email, data_nasc, telefone, apelido, senha) values ('maria', 'maria@gmail.com', '2000-10-05', '41 77777-7777', 'mariazinha', sha2('teste', 256));
insert into usuario (nome, email, data_nasc, telefone, apelido, senha) values ('joao', 'joao@gmail.com', '2000-07-05', '41 88888-8888', 'joaozao', sha2('teste', 256));


SELECT email, apelido, senha FROM usuario WHERE email = 'maria@gmail.com' OR apelido = 'mariazinha';
select * from usuario;