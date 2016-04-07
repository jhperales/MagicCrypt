import java.math.BigInteger;

public class Random
{
    private static BigInteger[] seed = new BigInteger[3];
    private static BigInteger[] xmod = new BigInteger[3];
    private static BigInteger tfs = new BigInteger("256");
    private static BigInteger recstates = new BigInteger("512").pow(1024);
    private static BigInteger[] dxmod = new BigInteger[]{new BigInteger("177"), new BigInteger("176"), new BigInteger("178")}
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
    public static BigInteger randint(BigInteger min, BigInteger max)
    {
        return randlong().mod(max.subtract(min)).add(min);
    }
    public static BigInteger randint(int min, int max)
    {
        return randint(new BigInteger(String.valueOf(min)), new BigInteger(String.valueOf(max)));
    }
    public static BigInteger randlong(){
        BigInteger x = seed[0];
        BigInteger y = seed[1];
        BigInteger z = seed[2];
        
        x = new BigInteger("171").multiply(x).mod(xmod[0]);
        y = new BigInteger("172").multiply(x).mod(xmod[1]);
        z = new BigInteger("170").multiply(x).mod(xmod[2]);
        
        seed[0] = x;
        seed[1] = y;
        seed[2] = z;
        
        return x.add(y).add(z).subtract(new BigInteger("3"));
    }
    public static void seed(BigInteger a, BigInteger b){
        while(a.abs().compareTo(b) < 0)
        {
            a = hash(String.valueOf(a)).multiply(b);
        }
        BigInteger x = a.mod(xmod[0]);
        a = a.divide(xmod[0]);
        BigInteger y = a.mod(xmod[1]);
        a = a.divide(xmod[1]);
        BigInteger z = a.mod(xmod[2]);
        a = a.divide(xmod[2]);
        
        seed[0] = x.add(BigInteger.ONE);
        seed[1] = y.add(BigInteger.ONE);
        seed[2] = z.add(BigInteger.ONE);
    }
    public static void seed(BigInteger a){
        seed(a, recstates);
    }
    public static void seed(){
        seed(millis().multiply(recstates));
    }
    
    public static BigInteger millis(){
        return new BigInteger(String.valueOf(System.currentTimeMillis()));
    }
    public static BigInteger hash(Object o){
        String s = String.valueOf(o);
        return stoi(s).and(new BigInteger("2").pow(128).subtract(BigInteger.ONE));
    }
}
