import java.util.Random;

public class SlidingWindowSimulation {
    private static final int WINDOW_SIZE = 5;
    private static final int MAX_PACKETS = 1000;
    private static final Random random = new Random();

    public static void main(String[] args) {
        int[] packetSizes = { 64, 128, 256, 512, 1024 }; // in bytes
        double[] errorRates = { 0.01, 0.05, 0.1 }; // packet loss probabilities
        int[] roundTripTimes = { 50, 100, 200 }; // in milliseconds

        for (int packetSize : packetSizes) {
            for (double errorRate : errorRates) {
                for (int rtt : roundTripTimes) {
                    double throughput = simulateSlidingWindow(packetSize, errorRate, rtt);
                    System.out.printf(
                            "Packet Size: %d bytes, Error Rate: %.2f, RTT: %d ms, Throughput: %.2f packets/s%n",
                            packetSize, errorRate, rtt, throughput);
                }
            }
        }
    }

    private static double simulateSlidingWindow(int packetSize, double errorRate, int rtt) {
        int packetsSent = 0;
        int packetsAcked = 0;
        int windowStart = 0;
        int windowEnd = WINDOW_SIZE;
        int currentTime = 0;

        while (packetsSent < MAX_PACKETS) {
            for (int i = windowStart; i < windowEnd && packetsSent < MAX_PACKETS; i++) {
                packetsSent++;
                if (random.nextDouble() > errorRate) {
                    packetsAcked++;
                }
            }

            windowStart += WINDOW_SIZE;
            windowEnd = Math.min(windowEnd + WINDOW_SIZE, MAX_PACKETS);
            currentTime += rtt;
        }

        return (double) packetsAcked / (currentTime / 1000.0); // packets per second
    }
}
