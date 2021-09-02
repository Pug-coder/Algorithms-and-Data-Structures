#include <stdio.h>
int main()
{   
	int n;
	long l, r, cl, cr;
	scanf("%i", &n);
	scanf("%li %li", &cl, &cr);
	for(int i = 0; i < n - 1; i++)
	{
		scanf("%li %li", &l, &r);
		if(l < cr && r > cr) cr = r;
		else if(l > cr + 1) 
		{
			printf("%li %li\n", cl, cr);
			cl = l;
			cr = r;
		}
	else if(l == cr + 1) cr = r;
	}	
	printf("%li %li", cl, cr);
	return 0;
}