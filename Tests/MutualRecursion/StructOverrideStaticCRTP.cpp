#include <iostream>

template<class T>
struct base
{
    static void n(int v)
    {
        std::cout << "n " << v;
    }

    static void m(int v)
    {
        T::n(v);
    }
};

struct derived : public base<derived>
{
    static void n(int v)
    {
        m(v);
    }
};

int main()
{
    derived::m(10);

    return 0;
}