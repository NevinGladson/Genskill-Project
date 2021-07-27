drop table if exists task; -- storing tasks
drop table if exists urgency; --to store urgency rating
drop table if exists task_status; --to store whether the task is complete or not
drop table if exists overdue_tasks; --to store the overdue tasks
drop table if exists user_auth; -- for user authetication
drop table if exists post; -- for user authentication

create table user_auth (
  id serial primary key,
  username text unique not null,
  password text not null
);

create table post (
  id serial primary key,
  author_id serial not null,
  created timestamp not null default current_timestamp,
  title text not null,
  body text not null,
  foreign key (author_id) references user_auth (id)
);

create table task_status (
       id serial primary key,
       status text
       );

create table urgency (
       id serial primary key,
       urgency text,
       terminal boolean
       );  

create table task(
    id serial primary key,
    task text not null,
    date_of_task date not null,
    day text,
    points text,
    urgency serial references urgency(id),
    status serial references task_status(id)
    );
    
create table overdue_tasks(
    id serial primary key,
    task text,
    points text
    );
    

insert into urgency (urgency, terminal) values  ('Very Important', FALSE);
insert into urgency (urgency, terminal) values  ('Important', FALSE);
insert into urgency (urgency, terminal) values  ('Normal', FALSE);
insert into urgency (urgency, terminal) values  ('Expendable', FALSE);

insert into task_status (status) values  ('Complete');
insert into task_status (status) values  ('Not Complete');
