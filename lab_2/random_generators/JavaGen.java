import java.util.Random;

public class JavaGen {

    public static int[] getRandBitArray(int size) {
        Random random = new Random();
        int[] res = new int[size];

        for (int i = 0; i < size; i++) {
            res[i] = random.nextInt(2);
        }

        return res;
    }


    public static void main(String[] args) {
        int size = 128;
        int[] res = getRandBitArray(size);

        for (int i = 0; i < res.length; i++) {
            System.out.print(res[i]);
        }
    }
}