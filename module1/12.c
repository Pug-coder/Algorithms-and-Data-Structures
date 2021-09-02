unsigned long peak(unsigned long nel,
        int (*less)(unsigned long, unsigned long))
{
        unsigned long left = 0, right = nel - 1, c = (left+right)/2;
        while(left <= right)
        {       
                int r , l;
                if(c == 0) 
                {
                        l = 0;
                        r = less(c, c+1);
                }
                else if(c == nel-1)
                {
                  r = 0;
                  l = less(c,c+1);      
                } 
                else
                {
                        r=less(c,c+1);
                        l=less(c,c-1);
                }
                if(r == 0 && l == 0) return c;
                else if(r == 0 && l == 1) right = c - 1;
                else if (r == 1 && l == 0) left = c + 1;
                else right = c - 1;
                c = (left+1)/2 + right/2;

        }
        return -1;
}