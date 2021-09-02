#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char **argv)
{
	if(argc != 4)
	{
		printf("Usage: frame <height> <width> <text>");
		return 0;
	}
	int h = atoi(argv[1]), w = atoi(argv[2]);
	char *t = argv[3];
	int c = strlen(t);
	if(h<=2 || w-2 < c)
	{
		printf("Error");
		return 0;	
	} 
	int sp = (w-2) - c;
	for(int i=0; i<w; i++) printf("*");
	printf("\n");
	h=h-2;
	for(int j=1; j<=h; j++)
	{
		if(j== (h+1)/2)
		{
			printf("*");
			for(int z =0; z< sp/2; z++) printf(" ");
			for(int z =0; z<c; z++) printf("%c", t[z]);
			for(int z =0; z< sp - sp/2; z++) printf(" ");	
			printf("*"); 
		}
		else
		{
			printf("*");
			for(int z =0; z<w-2; z++) printf(" ");
			printf("*");
		}
		printf("\n");	
	}
	for(int i=0; i<w; i++) printf("*");
	
	return 0;
}