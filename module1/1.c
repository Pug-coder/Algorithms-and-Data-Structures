#include <stdio.h>
int main(){
	int n, k;
	long x0, a, res; 
	scanf("%i %i %li", &n,&k,&x0);
	for(int i = 0; i < n-k+1; i++)
	{
		scanf("%li", &a);
		int p = n - i, s = p;
		for(int j=0; j<k; j++)
		{
			a*=s;
			s--;
		}
		if(i==0)
			res=a;
		else
			res=res*x0+a;
		
	}
	printf("%li", res);
return 0;
}