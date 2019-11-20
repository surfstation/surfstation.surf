import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.LinkedList;
import java.util.Date;
import java.nio.charset.Charset;

// cd surfstation.surf/data/ && javac wxdaily.java && java wxdaily .
public class wxdaily {
  public static void main(final String[] args) throws Exception {
    if (args.length != 1) {
      System.err.println("bad usage");
      System.exit(1);
    }
    final File dataDir = new File(args[0]);
    final String[][] files = {
      {"firstlight.txt", "firstLight"},
      {"sunrise.txt", "sunrise"},
      {"sunset.txt", "sunset"},
      {"lastlight.txt", "lastLight"},
      {"moonpercentvis.txt", "moonStatus"},
      {"tides.txt", "tides"},
    };
    final Date now = new Date();
    final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
    final String date = sdf.format(now);
    final StringBuilder result = new StringBuilder();
    result.append("{\n");
    for (int i=0; i<files.length; i++) {
      final Path filePath = new File(dataDir, files[i][0]).toPath();
      final List<String> lines = Files.readAllLines(filePath, StandardCharsets.UTF_8);
      if ("tides.txt".equals(files[i][0])) {
        final List<String> found = new LinkedList<String>();
        for (final String line : lines) {
          if (line.matches("^" + date + ".+")) {
            final String[] arr = line.split(" ");
            found.add("\"" + arr[1] + " " + arr[2] + " " + arr[3] + "\"");
          }
        }
        result.append("  \"" + files[i][1] + "\":" + found + "\n"); // the tides file is processed last, so do not add the trailing comma
      } else if("moonpercentvis.txt".equals(files[i][0])) {
        String prevLine = null;
        for (final String line : lines) {
          if (line.matches("^" + date + ".+")) {
            String val = line.split(" ")[1] + "%";
            final int foundPercentage = Integer.parseInt(line.split(" ")[1], 10);
            if (prevLine != null) {
              final int previousPercentage = Integer.parseInt(prevLine.split(" ")[1], 10);
              if (foundPercentage == 0) {
                val = "New Moon 0%";
              } else if (foundPercentage == 100) {
                val = "Full Moon 100%";
              } else if (previousPercentage < foundPercentage) {
                val = "Waxing " + foundPercentage + "%";
              } else if (previousPercentage > foundPercentage) {
                val = "Waning " + foundPercentage + "%";
              }
            }
            result.append("  \"" + files[i][1] + "\":\"" + val + "\",\n");
            break;
          }
          prevLine = line;
        }
      } else {
        for (final String line : lines) {
          if (line.matches("^" + date + ".+")) {
            result.append("  \"" + files[i][1] + "\":\"" + line.split(" ")[1] + "\",\n");
            break;
          }
        }
      }
    }
    result.append("}\n\n");
    Files.write(new File(dataDir, "daily.json").toPath(), result.toString().getBytes(Charset.forName("UTF-8")));
  }
}

