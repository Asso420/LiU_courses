
#include "plist.h"

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "threads/malloc.h"

#define P_size 1000

struct p_list
{
    value_p content[P_size];
    struct lock plist_lock;
};
struct p_list plist;

void proc_init(void)
{
    for (int i = 0; i < P_size; i++)
    {
        plist.content[i] = NULL;
    }
    lock_init(&plist.plist_lock);
}

key_t proc_insert(int parent, int child)
{
    lock_acquire(&plist.plist_lock);
    for (int i = 0; i < P_size; i++)
    {
        if (plist.content[i] == NULL)
        {
            plist.content[i] = (value_p)malloc(sizeof(struct processes));
            plist.content[i]->free = false;
            plist.content[i]->pid = child;
            plist.content[i]->parent = parent;
            sema_init(&plist.content[i]->sema, 0);
            plist.content[i]->status = -1;
            plist.content[i]->done = false;
            plist.content[i]->parent_done = false;
            lock_release(&plist.plist_lock);
            return child;
        }
    }
    lock_release(&plist.plist_lock);
    return -1;
}

value_p proc_wait(int child, int tid)
{
    lock_acquire(&plist.plist_lock);
    value_p proc = proc_find(child);

    if (proc != NULL)
    {
        if (!proc->free && proc->parent == tid)
        {
            lock_release(&plist.plist_lock);
            sema_down(&proc->sema);
            lock_acquire(&plist.plist_lock);
            proc->free = true;
        }
    }
    lock_release(&plist.plist_lock);
    return proc;
}

value_p proc_free(int tid)
{
    lock_acquire(&plist.plist_lock);
    value_p proc = proc_find(tid);
    if (proc != NULL)
    {
        proc_remove(proc->pid);
        proc->done = true;
        if (proc->parent_done)
        {
            proc->free = true;
            // proc_cleanup();
        }
    }
    lock_release(&plist.plist_lock);
    return proc;
}

void proc_exit(int tid, int status)
{
    lock_acquire(&plist.plist_lock);
    value_p proc = proc_find(tid);
    if (proc != NULL)
    {
        proc->status = status;
    }
    lock_release(&plist.plist_lock);
}

value_p proc_find(int id)
{
    // lock_acquire(&plist.plist_lock);
    for (int i = 0; i < P_size; i++)
    {
        if (plist.content[i] != NULL)
        {
            if (plist.content[i]->pid == id)
            {
                // lock_release(&plist.plist_lock);
                return plist.content[i];
            }
        }
    }
    // lock_release(&plist.plist_lock);
    return NULL;
}

value_p proc_remove(key_t id)
{
    // lock_acquire(&plist.plist_lock);
    if (id >= 0 && id < P_size)
    {
        // lock_acquire(&plist.plist_lock);
        for (int i = 0; i < P_size; i++)
        {
            value_p proc = proc_find(i);
            if (proc != NULL)
            {
                if (proc->parent == id)
                {
                    proc->parent_done = true;
                    if (proc->done)
                    {
                        proc->free = true;
                        // lock_release(&plist.plist_lock);
                        // proc_cleanup();
                        // lock_acquire(&plist.plist_lock);
                    }
                }
            }
        }
        // lock_release(&plist.plist_lock);
    }
    return NULL;
}

void proc_print(void)
{
    printf("FREE | PID | PARENT | SEMA | STATUS | DONE | PARENTDONE\n");
    printf("-------------------------------------------------------\n");
    lock_acquire(&plist.plist_lock);
    for (int i = 0; i < P_size; i++)
    {
        if (plist.content[i] != NULL)
        {
            printf("%4d |%4d |%7d |%5d |%7d |%5d | %d\n", plist.content[i]->free,
                   plist.content[i]->pid, plist.content[i]->parent, plist.content[i]->sema.value,
                   plist.content[i]->status, plist.content[i]->done, plist.content[i]->parent_done);
        }
    }
    lock_release(&plist.plist_lock);
    printf("-------------------------------------------------------\n");
}

void proc_cleanup(void)
{
    lock_acquire(&plist.plist_lock);
    for (int i = 0; i < P_size; i++)
    {
        if (plist.content[i] != NULL)
        {
            if (plist.content[i]->free)
            {
                free(plist.content[i]);
                plist.content[i] = NULL;
            }
        }
    }
    lock_release(&plist.plist_lock);
}