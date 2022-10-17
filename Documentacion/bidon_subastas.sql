create database bidon_subastas;
use bidon_subastas;

create table Usuarios
(
id_usuario int not null unique auto_increment,
Nombre varchar (25) not null,
Apellido varchar (25) not null,
email  varchar (128) not null,
usuario varchar (20) not null,
clave varchar (20) not null,
fecha_nac date not null,
tipo_usuario int not null,
primary key (id_usuario)
)
ENGINE = InnoDB;

alter table Usuarios auto_increment = 1;

create table Articulos
(
id_articulo int not null unique auto_increment,
titulo varchar (50) not null,
descripcion varchar (512) not null,
valuacion int not null,
id_consignatario int not null,
primary key (id_articulo),
constraint fk_id_consignatario
foreign key (id_consignatario) references Usuarios (id_usuario)
)
ENGINE = InnoDB;

alter table Articulos auto_increment = 1;

create table Subastas
(
id_subasta int not null unique auto_increment,
fecha date not null,
titulo varchar (50) not null,
descripcion varchar (512) not null,
imagen varchar (256) not null,
primary key (id_subasta)
)
ENGINE = InnoDB;

alter table Subastas auto_increment = 1;

create table Lotes
(
id_lote int not null unique auto_increment,
precio_base int not null,
orden int not null,
id_articulo int not null,
id_subasta int not null,
primary key (id_lote),
constraint fk_id_articulo
foreign key (id_articulo) references Articulos (id_articulo),
constraint fk_id_subasta
foreign key (id_subasta) references Subastas (id_subasta)
)
ENGINE = InnoDB;

alter table Lotes auto_increment = 1;

create table Pujas
(
id_puja int not null unique auto_increment,
monto int not null,
id_pujador int not null,
id_lote int not null,
primary key (id_puja),
constraint fk_id_pujador
foreign key (id_pujador) references Usuarios (id_usuario),
constraint fk_id_lote
foreign key (id_lote) references Lotes (id_lote)
)
ENGINE = InnoDB;

alter table Pujas auto_increment = 1;

create table Ventas
(
id_venta int not null unique auto_increment,
precio_final float not null,
comision float not null,
pago_consignatario float not null,
id_puja int not null,
primary key (id_venta),
constraint fk_id_puja
foreign key (id_puja) references Pujas (id_puja)
)
ENGINE = InnoDB;

alter table Ventas auto_increment = 1;

