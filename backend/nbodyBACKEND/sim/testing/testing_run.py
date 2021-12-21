import testing_nmath
import testing_nbody
import testing_integrators

def test_all():
    testing_nmath.test_main()
    testing_nbody.test_main()
    testing_integrators.test_main()
