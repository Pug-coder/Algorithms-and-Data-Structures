unsigned long binsearch(unsigned long nel, int (*compare)(unsigned long i))
{
	unsigned long left = 0, right = nel - 1, c = (left + right)/2;
	while(left <= right)
	{
		int ch = compare(c);
		if(ch == 1)
		{
			right = c - 1;
		}
		else if(ch == -1)
		{
			left = c+1;
		}
		else return c;
		c = (left + right)/2;
	}
	return nel;
}