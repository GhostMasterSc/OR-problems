import matplotlib.pyplot as plt
import numpy as np

class J_rule:
    def __init__(self, attrs, p_ratio=0.8):
        self.attrs = attrs
        self.p_ratio = p_ratio
    
    def sort_orders(self):
        not_visited = set(self.attrs.keys())
        sorted_orders_right = []
        sorted_orders_left = []
        while not_visited:
            min_value = float("inf")
            for jobs in not_visited:
                value = min(self.attrs[jobs]['prep'], self.attrs[jobs]['cook'])
                effective_value = value * (1 - self.p_ratio) if self.attrs[jobs]['kid'] else value
                if effective_value < min_value:
                    min_value = effective_value
                    Left = False if self.attrs[jobs]['prep'] < self.attrs[jobs]['cook'] else True
                    prep_time = self.attrs[jobs]['prep']
                    cooking_time = self.attrs[jobs]['cook']
                    order_id = jobs
            
            not_visited.remove(order_id)

            if Left:
                sorted_orders_left.insert(0, (order_id, prep_time, cooking_time))
            else:
                sorted_orders_right.append((order_id, prep_time, cooking_time))
        ordered = sorted_orders_right + sorted_orders_left

        return ordered
    
    def schedule_orders(self, p_ratio=None, print_results=True):
        if p_ratio is not None:
            self.p_ratio = p_ratio
        # Sort orders based on Johnson's Rule (minimum of prep or cook time)
        sorted_orders = self.sort_orders()
        
        prep_stations = [0, 0]  # Completion times for prep stations
        cook_stations = [0, 0]  # Completion times for cook stations
        
        completion_times = {}
        schedule = []

        for order in sorted_orders:
            order_id, prep_time, cooking_time = order
            if prep_stations[0] > prep_stations[1]:
                prep_start_time = prep_stations[1]
                prep_end_time = prep_start_time + prep_time
                prep_stations[1] = prep_end_time
                prep_station = 1
            else:
                prep_start_time = prep_stations[0]
                prep_end_time = prep_start_time + prep_time
                prep_stations[0] = prep_end_time
                prep_station = 0

            if cook_stations[0] > cook_stations[1]:
                cook_start_time = max(prep_end_time, cook_stations[1])
                cook_end_time = cook_start_time + cooking_time
                cook_stations[1] = cook_end_time
                cook_station = 1
            else:
                cook_start_time = max(prep_end_time, cook_stations[0])
                cook_end_time = cook_start_time + cooking_time
                cook_stations[0] = cook_end_time
                cook_station = 0

            schedule.append((order_id, prep_station, prep_start_time, prep_end_time, cook_station, cook_start_time, cook_end_time))

            completion_times[order_id] = cook_end_time

        total_time = max(max(prep_stations), max(cook_stations))
        
        self.completion_times = completion_times
        self.total_time = total_time
        self.schedule = schedule

        if print_results:
            print(f"Total time to complete all orders: {total_time} minutes")
            print("Order completion times:")
            for order_id, completion_time in sorted(completion_times.items()):
                print(f"Order {order_id}: {completion_time} minutes")
    
    def create_gantt_chart(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(self.attrs)))
        y_labels = ['Prep 1', 'Prep 2', 'Cook 1', 'Cook 2']
        
        for order in self.schedule:
            order_id, prep_station, prep_start, prep_end, cook_station, cook_start, cook_end = order
            
            # Plot prep task
            ax.barh(y_labels[prep_station], prep_end - prep_start, left=prep_start, 
                    color=colors[order_id], alpha=0.8)
            ax.text(prep_start + (prep_end - prep_start)/2, y_labels[prep_station], 
                    f'order {order_id}', ha='center', va='center', rotation=90)
            
            # Plot cook task
            ax.barh(y_labels[cook_station + 2], cook_end - cook_start, left=cook_start, 
                    color=colors[order_id], alpha=0.8)
            ax.text(cook_start + (cook_end - cook_start)/2, y_labels[cook_station + 2], 
                    f'order {order_id}', ha='center', va='center', rotation=90)
        
        ax.set_ylim(-1, len(y_labels))
        ax.set_xlim(0, self.total_time)
        ax.set_xlabel('Time (minutes)')
        ax.set_title('Order Processing Schedule')
        ax.grid(True)
        
        plt.tight_layout()
        plt.show()

    def plot_completion_times(self):
        p_ratios = np.linspace(0, 1, 20)
        completion_times = []

        for p_ratio in p_ratios:
            self.schedule_orders(p_ratio, print_results=False)
            completion_times.append(self.total_time)

        plt.figure(figsize=(10, 6))
        plt.plot(p_ratios, completion_times, marker='o')
        plt.xlabel('Priority Ratio (p_ratio)')
        plt.ylabel('Total Completion Time')
        plt.title('Total Completion Time vs. Priority Ratio (p_ratio)')
        plt.grid(True)
        plt.show()

# Given attributes
attrs = {0: {"kid": True, "prep": 5, "cook": 20},
         1: {"kid": False, "prep": 15, "cook": 15},
         2: {"kid": True, "prep": 20, "cook": 25},
         3: {"kid": True, "prep": 5, "cook": 55},
         4: {"kid": True, "prep": 40, "cook": 45},
         5: {"kid": False, "prep": 45, "cook": 35},
         6: {"kid": False, "prep": 50, "cook": 55},
         7: {"kid": False, "prep": 5, "cook": 10},
         8: {"kid": True, "prep": 10, "cook": 10},
         9: {"kid": True, "prep": 55, "cook": 30},
         10: {"kid": False, "prep": 25, "cook": 20},
         11: {"kid": True, "prep": 30, "cook": 40},
         12: {"kid": False, "prep": 15, "cook": 5},
         13: {"kid": True, "prep": 35, "cook": 15}}

# Instantiate the class
jr = J_rule(attrs)

# Plot the completion times
jr.plot_completion_times()

# Run schedule_orders outside of the plotting function
jr.schedule_orders(print_results=True)

# Create Gantt chart
jr.create_gantt_chart()
