import tensorflow as tf

# referer : https://www.tensorflow.org/guide/variable?hl=ko
def print_1():
    a = tf.constant(10)
    b = tf.constant(32)
    tf.print((a + b))

def print_2():
    node1 = tf.constant(3.0, dtype=tf.float32)
    node2 = tf.constant(4.0)
    tf.print(node1, node2)

def print_3():
    my_tensor = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    my_variable = tf.Variable(my_tensor)

    # Variables can be all kinds of types, just like tensors
    bool_variable = tf.Variable([False, False, False, True])
    complex_variable = tf.Variable([5 + 4j, 6 + 1j])

    print("Shape: ", my_variable.shape)
    print("DType: ", my_variable.dtype)
    print("As NumPy: ", my_variable.numpy)

def print_4():
    a = tf.Variable([2.0, 3.0])
    # Create b based on the value of a
    b = tf.Variable(a)
    a.assign([5, 6])

    # a and b are different
    print('a.numpy()', a.numpy())
    print('b.numpy()', b.numpy())

    # There are other versions of assign
    print(a.assign_add([2, 3]).numpy())  # [7. 9.]
    print(a.assign_sub([7, 9]).numpy())  # [0. 0.]

def print_5():
    my_tensor = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    # Create a and b; they have the same value but are backed by different tensors.
    a = tf.Variable(my_tensor, name="Mark")
    # A new variable with the same name, but different value
    # Note that the scalar add is broadcast
    b = tf.Variable(my_tensor + 1, name="Mark")

    # These are elementwise-unequal, despite having the same name
    print(a == b)

if __name__ == '__main__':
    # print_1()
    # print_2()
    # print_3()
    # print_4()
    print_5()


