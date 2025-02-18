import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

def ripple_carry_adder(A, B):
    carry = 0
    result = [0] * len(A)

    start_time = time.perf_counter_ns()

    for i in range(len(A)):
        sum_bit = A[i] ^ B[i] ^ carry
        carry = (A[i] & B[i]) | (carry & (A[i] ^ B[i]))
        result[i] = sum_bit

    execution_time_ns = time.perf_counter_ns() - start_time

    return result, execution_time_ns

def generate_g_and_p(A, B):
    g = [A[i] & B[i] for i in range(len(A))]
    p = [A[i] | B[i] for i in range(len(A))]
    return g, p

def carry_lookahead_adder(A, B, G, P):
    c = [0] * (len(A) + 1)
    s = [0] * len(A)

    start_time = time.perf_counter_ns()

    c[0] = 0  # Initial carry-in

    for i in range(len(A)):
        c[i + 1] = G[i] | (P[i] & c[i])
        s[i] = A[i] ^ B[i] ^ c[i]

    execution_time_ns = time.perf_counter_ns() - start_time

    return s, execution_time_ns

def calculate():
    try:
        A = [int(bit) for bit in entry_a.get()]
        B = [int(bit) for bit in entry_b.get()]

        # Check if A and B have more than 6 bits
        if len(A) > 6 or len(B) > 6:
            messagebox.showerror("Error", "Binary operands must have a maximum of 6 bits.")
            return  # Exit the function

        # Check if A and B have the same length
        if len(A) != len(B):
            messagebox.showerror("Error", "Binary operands must have the same number of bits.")
            return  # Exit the function

        G, P = generate_g_and_p(A, B)  # Generate G and P here
        result_ripple, execution_time_ripple_ns = ripple_carry_adder(A, B)
        result_cla, execution_time_cla_ns = carry_lookahead_adder(A, B, G, P)  # Pass G and P

        result_frame = ttk.LabelFrame(root, text="Results")
        result_frame.grid(column=0, row=3, padx=10, pady=10)

        ttk.Label(result_frame, text="Ripple Carry Adder Result:").grid(column=0, row=0, sticky='w', padx=5)
        ttk.Label(result_frame, text="Operand A:").grid(column=0, row=1, sticky='w', padx=5)
        ttk.Label(result_frame, text="Operand B:").grid(column=0, row=2, sticky='w', padx=5)
        ttk.Label(result_frame, text="Result:").grid(column=0, row=3, sticky='w', padx=5)
        ttk.Label(result_frame, text="Execution Time:").grid(column=0, row=4, sticky='w', padx=5)

        ttk.Label(result_frame, text=''.join(map(str, A)).ljust(30)).grid(column=1, row=1, columnspan=4, padx=5)
        ttk.Label(result_frame, text=''.join(map(str, B)).ljust(30)).grid(column=1, row=2, columnspan=4, padx=5)
        ttk.Label(result_frame, text=''.join(map(str, result_ripple)).ljust(30)).grid(column=1, row=3, columnspan=4, padx=5)
        ttk.Label(result_frame, text=f'{execution_time_ripple_ns} ns'.ljust(30)).grid(column=1, row=4, columnspan=4, padx=5)

        ttk.Label(result_frame, text="").grid(column=0, row=5)  # Empty row for spacing

        ttk.Label(result_frame, text="Carry Look-Ahead Adder Result:").grid(column=0, row=6, sticky='w', padx=5)
        ttk.Label(result_frame, text="Operand A:").grid(column=0, row=7, sticky='w', padx=5)
        ttk.Label(result_frame, text="Operand B:").grid(column=0, row=8, sticky='w', padx=5)
        ttk.Label(result_frame, text="Result:").grid(column=0, row=9, sticky='w', padx=5)
        ttk.Label(result_frame, text="Execution Time:").grid(column=0, row=10, sticky='w', padx=5)

        ttk.Label(result_frame, text=''.join(map(str, A)).ljust(30)).grid(column=1, row=7, columnspan=4, padx=5)
        ttk.Label(result_frame, text=''.join(map(str, B)).ljust(30)).grid(column=1, row=8, columnspan=4, padx=5)
        ttk.Label(result_frame, text=''.join(map(str, result_cla)).ljust(30)).grid(column=1, row=9, columnspan=4, padx=5)
        ttk.Label(result_frame, text=f'{execution_time_cla_ns} ns'.ljust(30)).grid(column=1, row=10, columnspan=4, padx=5)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid binary operands (0s and 1s only).")

root = tk.Tk()
root.title("Binary Adder")

main_frame = ttk.Frame(root, padding=20)
main_frame.grid(column=0, row=0, sticky=("N", "W", "E", "S"))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(main_frame, text="Binary Adder", font=("Helvetica", 16)).grid(column=0, row=0, columnspan=2, pady=10)
ttk.Label(main_frame, text="Enter binary operand A (e.g., 1011, max 6 bits):").grid(column=0, row=1, sticky='w', padx=5)
entry_a = ttk.Entry(main_frame)
entry_a.grid(column=1, row=1, padx=5)
ttk.Label(main_frame, text="Enter binary operand B (e.g., 0111, max 6 bits):").grid(column=0, row=2, sticky='w', padx=5)
entry_b = ttk.Entry(main_frame)
entry_b.grid(column=1, row=2, padx=5)
calculate_button = ttk.Button(main_frame, text="Calculate", command=calculate)
calculate_button.grid(column=0, row=3, columnspan=2, pady=10)

root.mainloop()
