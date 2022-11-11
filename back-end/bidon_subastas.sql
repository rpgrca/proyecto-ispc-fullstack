create database bidon_subastas;
use bidon_subastas;

create table Usuarios
(
id int not null unique auto_increment,
nombre varchar (25) not null,
apellido varchar (25) not null,
email  varchar (128) not null,
usuario varchar (20) not null,
clave varchar (20) not null,
nacimiento date not null,
tipo_usuario int not null,
primary key (id)
)
ENGINE = InnoDB;

alter table Usuarios auto_increment = 1;

create table Articulos
(
id int not null unique auto_increment,
titulo varchar (50) not null,
descripcion varchar (512) not null,
valuacion int not null,
id_consignatario int not null,
primary key (id),
constraint fk_id_consignatario
foreign key (id_consignatario) references Usuarios (id)
)
ENGINE = InnoDB;

alter table Articulos auto_increment = 1;

create table Subastas
(
id int not null unique auto_increment,
fecha date not null,
titulo varchar (50) not null,
descripcion varchar (512) not null,
imagen varchar (256) not null,
primary key (id)
)
ENGINE = InnoDB;

alter table Subastas auto_increment = 1;

create table Lotes
(
id int not null unique auto_increment,
precio_base int not null,
orden int not null,
id_articulo int not null,
id_subasta int not null,
primary key (id),
constraint fk_id_articulo
foreign key (id_articulo) references Articulos (id),
constraint fk_id_subasta
foreign key (id_subasta) references Subastas (id)
)
ENGINE = InnoDB;

alter table Lotes auto_increment = 1;

create table Pujas
(
id int not null unique auto_increment,
monto int not null,
id_pujador int not null,
id_lote int not null,
primary key (id),
constraint fk_id_pujador
foreign key (id_pujador) references Usuarios (id),
constraint fk_id_lote
foreign key (id_lote) references Lotes (id)
)
ENGINE = InnoDB;

alter table Pujas auto_increment = 1;

create table Ventas
(
id int not null unique auto_increment,
precio_final float not null,
comision float not null,
pago_consignatario float not null,
id_puja int not null,
primary key (id),
constraint fk_id_puja
foreign key (id_puja) references Pujas (id)
)
ENGINE = InnoDB;

alter table Ventas auto_increment = 1;

