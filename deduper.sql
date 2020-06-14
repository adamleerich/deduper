


drop table if exists [scan];
drop table if exists [md5];

create table if not exists [scan] (
    [scan_id] int not null
   ,[device] varchar(256) not null
   ,[command] varchar(1024) not null
   ,[scan_start] datetime null
   ,[scan_end] datetime null
   ,[scan_status] varchar(1024) null
   ,constraint [PK__scan] primary key ([scan_id])
);
create table if not exists [md5] (
   [scan_id] int not null
  ,[file] varchar(1024) not null
  ,[md5] char(32) not null
  ,[last_modified] datetime not null
  ,[last_hashed] datetime not null
  ,constraint [PK__md5] primary key ([scan_id], [file])
  ,constraint [FK__md5_scan_id] foreign key ([scan_id]) references [scan]([scan_id])
);
create index [IN__md5_md5] on [md5]([md5]);
