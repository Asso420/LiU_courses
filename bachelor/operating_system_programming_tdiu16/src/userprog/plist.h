#ifndef _PLIST_H_
#define _PLIST_H_


/* Place functions to handle a running process here (process list).

   plist.h : Your function declarations and documentation.
   plist.c : Your implementation.

   The following is strongly recommended:

   - A function that given process inforamtion (up to you to create)
     inserts this in a list of running processes and return an integer
     that can be used to find the information later on.

   - A function that given an integer (obtained from above function)
     FIND the process information in the list. Should return some
     failure code if no process matching the integer is in the list.
     Or, optionally, several functions to access any information of a
     particular process that you currently need.

   - A function that given an integer REMOVE the process information
     from the list. Should only remove the information when no process
     or thread need it anymore, but must guarantee it is always
     removed EVENTUALLY.

   - A function that print the entire content of the list in a nice,
     clean, readable format.

 */

#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <threads/synch.h>


typedef struct processes* value_p; //value_t represents: values stored in the data structure
typedef int key_t; // ket_t represents the identifier to for processes

struct processes {
  bool free;
  int pid;
  int parent;
  struct semaphore sema;
  int status;
  bool done;
  bool parent_done;
}; 



void proc_init(void); 
key_t proc_insert(int parent, int child);
value_p proc_wait(int child, int tid);
void proc_exit(int tid, int status);
value_p proc_free(int tid);
value_p proc_find(int id);
value_p proc_remove(key_t id); 
void proc_print(void);
void proc_cleanup(void);

#endif


