#include "map.h"
#include <stdio.h>

void map_init(struct map* m)
{
    for (int i = 0; i < MAP_SIZE; i++)
    {
        m->content[i] = NULL;
    }
}

key_t map_insert(struct map* m, value_t v)
{
    for (int i = 0; i < MAP_SIZE; i++)
    {
        if (m->content[i] == NULL)
        {
            m->content[i]= v;
            return i;
        }
    }
    return -1;
}

value_t map_find(struct map* m, key_t k) {
    if (k >= 0 && k <= MAP_SIZE ) 
    {
        if (m->content[k] != NULL) 
        { 
            return m->content[k];  
        } 
    }
    return NULL;
}

value_t map_remove(struct map* m, key_t k) { 
    if (k >= 0 && k < MAP_SIZE ) 
    {
        //printf("hjkfdjk");
        if (m->content[k] != NULL)  
        { 
            value_t removed_value = m->content[k];
            m->content[k] = NULL;
            //printf("k värde %d", k);
            return removed_value;  
        } 
    }
    return NULL;
}

void map_for_each(struct map* m, void (*exec)(key_t k, value_t v, int aux), int aux)
{
    for (int i = 0; i < MAP_SIZE; i++)
    {
        if (m->content[i] != NULL)
        {
            (*exec)(i,m->content[i], aux);
        }
    }
}


void map_remove_if(struct map* m, bool (*cond)(key_t k, value_t v, int aux), int aux)
{
    for(int i = 0; i < MAP_SIZE; i++)
    {
        if((*cond)(i, m->content[i], aux))
        {
            map_remove(m, i);
        }
    }
}
