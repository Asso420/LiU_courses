#include <stdio.h>
#include <syscall-nr.h>
#include "userprog/syscall.h"
#include "threads/interrupt.h"
#include "threads/thread.h"

/* header files you probably need, they are not used yet */
#include <string.h>
#include "filesys/filesys.h"
#include "filesys/file.h"
#include "threads/vaddr.h"
#include "threads/init.h"
#include "userprog/pagedir.h"
#include "userprog/process.h"
#include "devices/input.h"
#include "devices/timer.h"
#include "userprog/plist.h"


static void syscall_handler (struct intr_frame *);

void
syscall_init (void)
{
  intr_register_int (0x30, 3, INTR_ON, syscall_handler, "syscall");
}


/* This array defined the number of arguments each syscall expects.
   For example, if you want to find out the number of arguments for
   the read system call you shall write:

   int sys_read_arg_count = argc[ SYS_READ ];

   All system calls have a name such as SYS_READ defined as an enum
   type, see `lib/syscall-nr.h'. Use them instead of numbers.
 */
const int argc[] = {
  /* basic calls */
  0, 1, 1, 1, 2, 1, 1, 1, 3, 3, 2, 1, 1,
  /* not implemented */
  2, 1,    1, 1, 2, 1, 1,
  /* extended, you may need to change the order of these two (plist, sleep) */
  0, 1
};

static
bool verify_fix_length(void* start, unsigned length) //checks all adresses if valid
{
  void* endAddr = (void*)((unsigned)start + length - 1);
  void* firstPage = pg_round_down(start);
  if (start == NULL || is_kernel_vaddr(start) || is_kernel_vaddr(endAddr))
  {
    return false;
  }

  for (void* addr = firstPage; addr <= endAddr; addr = (void*)((unsigned)addr + PGSIZE)) 
  {
    if (pagedir_get_page(thread_current()->pagedir, addr) == NULL) 
    {
      return false;
    }
  }

  return true;
}

static
bool verify_variable_length(char* start)
{
  uintptr_t currentPage = pg_no(start);
  if (pagedir_get_page(thread_current()->pagedir, start) == NULL || is_kernel_vaddr(start))
  {
    return false;
  }
  while(true)
  {
    char* currentAddr = start;
    if (currentPage != pg_no(currentAddr)) 
    {
      currentPage = pg_no(currentAddr);
      if (pagedir_get_page(thread_current()->pagedir, currentAddr) == NULL)
      {
        return false;
      }
    }
    if (*currentAddr == '\0') 
    {
      return true;
    }
    start++;
  }

}

static int syscall_read(int fd, void *buf, off_t len){
  char *buffer = (char *)buf;

  if(fd == STDOUT_FILENO || fd > 32 || fd < 0){
    return -1;
  }
  else if(fd == STDIN_FILENO){
    for(off_t i = 0; i < len; i++){
      buffer[i] = input_getc();
      if(buffer[i] == '\r'){
        buffer[i] = '\n';
      }
      putbuf(&buffer[i], 1);
    }
  }
  else{
    struct file *file = map_find(&(thread_current()->f_map), fd);
    if(file == NULL){
      return -1;
    }
    else{
      return file_read(file, buf, len);
    }
  }
  return len;
}

static int syscall_write(int fd, const void *buf, off_t len){
  char *buffer = (char *)buf;
  
  if(fd == STDIN_FILENO || fd > 32 || fd < 0){
    return -1;
  }
  else if(fd == STDOUT_FILENO){
    putbuf(buffer, len);
  }
  else{
    struct file *file = map_find(&(thread_current()->f_map), fd);
    if(file == NULL){
      return -1;
    }
    else{
      return file_write(file, buf, len);
    }
  }
  return len;
}

static int syscall_open(const char *name) {
    struct file *file = filesys_open(name);
    if (file == NULL) {
        return -1;
    } 
    int fd = map_insert(&(thread_current()->f_map), file);
    
    //printf("FD: %d\n", fd);
    return fd;
}

static void syscall_close(int fd) {
  struct file *file = map_remove(&(thread_current()->f_map), fd);
  filesys_close(file);
}

static int syscall_filesize(int fd){
  struct file *file = map_find(&(thread_current()->f_map), fd);
  return file_length(file);
}


static void syscall_seek(int fd, unsigned pos){

  struct file *file = map_find(&(thread_current()->f_map), fd);
  if(pos < (unsigned) file_length(file))
    file_seek(file, pos);
}

static unsigned syscall_tell(int fd){
  struct file *file = map_find(&(thread_current()->f_map), fd);
  if (file == NULL) {
    return -1;
  } 
  return file_tell(file);
}

static void
syscall_handler (struct intr_frame *f)
{

  int32_t* esp = (int32_t*)f->esp;
  
  if(!verify_fix_length((void*)esp, sizeof(*esp)))
  {
    thread_exit();
  }
  if(esp[0] < 0 || esp[0] >= SYS_NUMBER_OF_CALLS)
  {
    thread_exit();
  }
  if(!verify_fix_length((void*)esp, sizeof(*esp) * (argc[esp[0]]+ 1)))
  {
    thread_exit();
  }
  

  switch (*esp) 
  {
    case SYS_HALT: 
    {
      power_off();
      break;
    }
    case SYS_EXIT: 
    {
      process_exit(esp[1]);
      thread_exit();
      break;
    }
    case SYS_READ: 
    {
      // int fd = esp[1];
      // void *buf = (void *)esp[2];
      // unsigned len = esp[3];
      if (!verify_fix_length((void *)esp[2], esp[3])) 
      {
        thread_exit();
      }
      f->eax = syscall_read(esp[1], (void *)esp[2], esp[3]);
      break;
    }
    case SYS_WRITE:
    {
      // int fd = esp[1];
      // void *buf = (void *)esp[2];
      // unsigned len = esp[3];
      if (!verify_fix_length((void *)esp[2], esp[3])) 
      {
        thread_exit();
      }
      f->eax = syscall_write(esp[1], (void *)esp[2], esp[3]);
      break;
    }

    case SYS_OPEN:
    {
      char *name = (char *)esp[1];
      if (!verify_variable_length(name)) 
      {
        thread_exit();
      }     
      f->eax = syscall_open(name);
      break;
    }
    
    case SYS_CLOSE:
    {
      //int fd = esp[1];
      syscall_close(esp[1]);
      //printf("CLOSED: %d\n", esp[1]);
      break;
    }
    case SYS_CREATE:
    {
      char* name = (char*)esp[1];
      if (!verify_variable_length(name)) 
      {
        thread_exit();
      }   
      f->eax = filesys_create(name, esp[2]);
      break;
    }
    case SYS_REMOVE:
    {
      char* name = (char*)esp[1];
      if (!verify_variable_length(name)) 
      {
        thread_exit();
      }
      f->eax = filesys_remove(name);
      break;
    }
    case SYS_SEEK:
    { 
      syscall_seek(esp[1], esp[2]);
      break;
    }
    case SYS_TELL:
    {
      f->eax = syscall_tell(esp[1]);
      break;
    }
    case SYS_FILESIZE:
    {
      f->eax = syscall_filesize(esp[1]);
      break;
    }
    case SYS_EXEC:
    {
      char* cmd_line = (char*)esp[1];
      if (!verify_variable_length(cmd_line)) 
      {
        thread_exit();
      }
      f->eax = process_execute((char*)esp[1]);
      break;
    }
    case SYS_SLEEP:
    {
      timer_msleep(esp[1]);
      break;
    }
    case SYS_PLIST:
    {
      proc_print();
      break;
    }
    case SYS_WAIT:
    {
      f->eax = process_wait(esp[1]);
      break;
    }

    default:
    {
      printf ("Executed an unknown system call!\n");
      printf ("Stack top + 0: %d\n", esp[0]);
      printf ("Stack top + 1: %d\n", esp[1]);
      //power_off();     //Halt
      thread_exit();
    }

  }
}
