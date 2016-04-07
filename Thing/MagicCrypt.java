import java.math.BigInteger;
import java.lang.StringBuilder;

public class MagicCrypt
{
    private static BigInteger tfs = new BigInteger("256");
    public static BigInteger stoi(String f)
    {
        BigInteger ret = BigInteger.ZERO;
        for (int i = 0; i < f.length(); i++)
        {
            ret = ret.add(new BigInteger(String.valueOf(f.charAt(i))));
            ret = ret.multiply(tfs);
        }
        ret = ret.divide(tfs);
        return ret;
    }
    
    public static String itos(BigInteger f)
    {
        String ret = "";
        while (BigInteger.ZERO.compareTo(f) < 0)
        {
            ret += (char)(f.mod(tfs).intValue());
            f = f.divide(tfs);
        }
        return new StringBuilder(ret).reverse().toString();
    }
    
    
}
    