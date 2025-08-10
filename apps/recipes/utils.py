from io import BytesIO
import base64
import matplotlib.pyplot as plt

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    plt.close()  # Close the plot to free memory
    return graph

def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(6,3))

    if chart_type == 'bar':
        if 'category' in data.columns and 'count' in data.columns:
            plt.bar(data['category'], data['count'])
            plt.xlabel('Category')
            plt.ylabel('Count')
            plt.title('Bar Chart of Recipes by Category')
        elif 'date_created' in data.columns and 'quantity' in data.columns:
            plt.bar(data['date_created'], data['quantity'])
            plt.xlabel('Date Created')
            plt.ylabel('Quantity')
            plt.title('Bar Chart of Quantity Over Time')
        else:
            print('Data format not recognized for bar chart')

    elif chart_type == 'pie':
        labels = kwargs.get('labels', [])
        if 'count' in data.columns:
            plt.pie(data['count'], labels=labels)
            plt.title('Pie Chart')
        elif 'price' in data.columns:
            plt.pie(data['price'], labels=labels)
            plt.title('Pie Chart of Prices')
        else:
            print('Data format not recognized for pie chart')

    elif chart_type == 'line':
        if 'date_created' in data.columns and 'price' in data.columns:
            plt.plot(data['date_created'], data['price'])
            plt.xlabel('Date Created')
            plt.ylabel('Price')
            plt.title('Line Chart of Price Over Time')
        elif 'date_added' in data.columns and 'count' in data.columns:
            plt.plot(data['date_added'], data['count'])
            plt.xlabel('Date Added')
            plt.ylabel('Count')
            plt.title('Line Chart of Recipes Added Over Time')
        else:
            print('Data format not recognized for line chart')
    else:
        print('Unknown chart type')

    plt.tight_layout()
    chart = get_graph()
    return chart
