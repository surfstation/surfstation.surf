import java.util.*;
import java.io.*;

// javac tides.java && grep -v '#' tides.txt | java tides

public class tides {
  public static void main(final String[] args) throws Exception {
  final Map<String, List<String>> map = new TreeMap<String, List<String>>();
  final BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
  String line = null;
  while((line = stdin.readLine()) != null) {
    final String[] s = line.split(" ");
    final String key = "\"" + s[0] + "\"";
    List<String> t = map.get(key);
    if(t == null) {
      t = new ArrayList<String>();
      map.put(key, t);
    }
    t.add("\"" + s[1] + " " + s[2] + " " + s[3] + "\"");
  }
  stdin.close();
  System.out.println(map);
  }
}

