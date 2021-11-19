
/*
+package sandbox
+alias stdout org.eolang.io.stdout
+alias sprintf org.eolang.txt.sprintf

[] > base_factory
  [] > get_base
    memory > x
    [self v] > n
      x.write v > @
    [self v] > m
      self.n self v > @

[] > derived
  base_factory.get_base > @
  [self v] > n
    self.m self v > @
 */

class BaseFactory {
public:
    class GetBase {
    public:
        int x;

        GetBase() {
            this->x = 0;
        }

        virtual void n(int v) {
            this->x = v;
        }

        void m(int v) {
            this->n(v);
        }
    };
};

class Derived : public BaseFactory::GetBase {
public:
    void n(int v) override {
        this->m(v);
    }
};


int main() {
    auto* derivedInstance = new Derived();
    derivedInstance->m(12);

    return 0;
}
