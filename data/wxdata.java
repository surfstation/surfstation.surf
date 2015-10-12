import java.io.BufferedReader;
import java.io.InputStreamReader;

// javac wxdata.java
// java wxdata < surfstation.surf/data/sunrise.txt > surfstation.surf/data/tmp; mv surfstation.surf/data/tmp surfstation.surf/data/sunrise.txt;
public class wxdata {
  public static void main(final String[] args) throws Exception {
    final BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
    String line = null;
    while ((line = stdin.readLine()) != null) {
      final String daylightSavingsStart = "2016-03-13";
      final String daylightSavingsEnd = "2016-11-06";
      final String[] parts = line.split(" ");
      int time = Integer.parseInt(parts[1], 10);
      if ((0 <= parts[0].compareTo(daylightSavingsStart)) && (parts[0].compareTo(daylightSavingsEnd) < 0)) {
        time += 100;
      }
      int hours = time / 100;
      String ampm = (hours >= 12) ? "pm" : "am";
      if (hours > 12) {
        hours -= 12;
      } else if (hours == 0) {
        hours = 12;
      }
      final int minutes = time % 100;
      final String hoursStr = ((hours < 10) ? "0" : "") + hours;
      final String minutesStr = ((minutes < 10) ? "0" : "") + minutes;
      String result = parts[0] + " " + hoursStr + ":" + minutesStr + ampm;
      System.out.println(result);
    }
    stdin.close();
  }
}

