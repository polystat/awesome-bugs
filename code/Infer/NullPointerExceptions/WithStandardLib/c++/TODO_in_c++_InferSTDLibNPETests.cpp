//import java.io.File;
//import java.io.FileInputStream;
//import java.io.FileOutputStream;
//import java.io.IOException;
//import java.nio.channels.FileChannel;
//import java.nio.channels.FileLock;
//import java.util.HashMap;
//import java.util.concurrent.locks.Lock;
//
//public class InferSTDLibNPETests {
//
//    public static void nullPointerExceptionFromFaillingResourceConstructor() throws IOException {
//        FileInputStream fis = null;
//        try {
//            fis = new FileInputStream(new File("whatever.txt"));
//        } catch (IOException e) {
//        } finally {
//            fis.close();
//        }
//    }
//
//    public static void nullPointerExceptionFromFailingFileOutputStreamConstructor()
//        throws IOException {
//            FileOutputStream fos = null;
//        try {
//            fos = new FileOutputStream(new File("whatever.txt"));
//        } catch (IOException e) {
//        } finally {
//            fos.close();
//        }
//    }
//
//    String hashmapNPE(HashMap h, Object o) {
//        return (h.get(o).toString());
//    }
//
//    String NPEhashmapProtectedByContainsKey(HashMap h, Object o) {
//        if (h.containsKey(o)) {
//            return (h.get(o).toString());
//        }
//        return "aa";
//    }
//
//    int NPEvalueOfFromHashmapBad(HashMap<Integer, Integer> h, int position) {
//        return h.get(position);
//    }
//
//    Integer NPEvalueOfFromHashmapGood(HashMap<Integer, Integer> h, int position) {
//        return h.get(position);
//    }
//
//    public void testSystemGetPropertyReturn() {
//        String s = System.getProperty("");
//        int n = s.length();
//    }
//
//    int nullListFiles(String pathname) {
//        File dir = new File(pathname);
//        File[] files = dir.listFiles();
//        return files.length; // expect possible NullPointerException as files == null is possible
//    }
//
//    String nullTryLock(FileChannel chan) throws IOException {
//        FileLock lock = chan.tryLock();
//        return lock.toString(); // expect possible NullPointerException as lock == null is possible
//    }
//
//    String tryLockThrows(FileChannel chan) {
//        try {
//            FileLock lock = chan.tryLock();
//            return (lock != null ? lock.toString() : "");
//        } catch (IOException e) {
//            Object o = null;
//            return o.toString(); // expect NullPointerException as tryLock can throw
//        }
//    }
//
//    void dereferenceAfterUnlock1(Lock l) {
//        l.unlock();
//        String s = l.toString();
//        s = null;
//        s.toString(); // Expect NPE here
//    }
//
//    void dereferenceAfterUnlock2(Lock l) {
//        synchronized (l) {
//        String b = null;
//        }
//        String s = l.toString();
//        s = null;
//        s.toString(); // Expect NPE here
//    }
//
//
//}