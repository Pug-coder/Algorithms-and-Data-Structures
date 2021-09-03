#include <stdio.h>
int maxarray(void  *base, unsigned long nel, unsigned long width,
        int (*compare)(void *a, void *b))
{

       void *max = base;
       int indmax =0;
       for(int i=0; i<nel; i++)
       {
       	void *l = base +i*width;
       	if(compare(max, l)<0)
       	{
       		max = l;
       		indmax=i;      	
        }
       } 
       
return indmax;

}