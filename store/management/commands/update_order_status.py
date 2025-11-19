from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
# Removed: render_to_string, EmailMessage, HTML, CSS (since you don't want the bill)

# Ensure these imports match your actual model paths
from store.models.order import OrderDetail
from store.models.customer import Customer


class Command(BaseCommand):
    help = 'Updates the status of orders based on elapsed time.'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Define the elapsed time thresholds (10 second intervals for a 40s cycle)
        time_accepted = now - timedelta(seconds=10)
        time_packed = now - timedelta(seconds=20)
        time_on_the_way = now - timedelta(seconds=30)
        time_delivered = now - timedelta(seconds=40)

        self.stdout.write(self.style.MIGRATE_HEADING('--- Starting Accelerated Order Status Update Simulation ---'))

        # 1. Update Pending -> Accepted
        accepted_orders = OrderDetail.objects.filter(
            status='Pending',
            ordered_date__lte=time_accepted
        )
        count_accepted = accepted_orders.update(status='Accepted')
        self.stdout.write(self.style.SUCCESS(f'✅ Updated {count_accepted} orders to Accepted.'))

        # 2. Update Accepted -> Packed
        packed_orders = OrderDetail.objects.filter(
            status='Accepted',
            ordered_date__lte=time_packed
        )
        count_packed = packed_orders.update(status='Packed')
        self.stdout.write(self.style.SUCCESS(f'📦 Updated {count_packed} orders to Packed.'))

        # 3. Update Packed -> On The Way
        on_the_way_orders = OrderDetail.objects.filter(
            status='Packed',
            ordered_date__lte=time_on_the_way
        )
        count_on_the_way = on_the_way_orders.update(status='On The Way')
        self.stdout.write(self.style.SUCCESS(f'🚚 Updated {count_on_the_way} orders to On The Way.'))

        # 4. Update On The Way -> Delivered (Message Update Only)
        delivered_orders = OrderDetail.objects.filter(
            status='On The Way',
            ordered_date__lte=time_delivered
        )
        # Update the status
        count_delivered = delivered_orders.update(status='Deliverd')

        # Print the final success message
        if count_delivered > 0:
            self.stdout.write(self.style.SUCCESS(f'🎉 Updated {count_delivered} orders to Deliverd. No bill sent.'))

        self.stdout.write(self.style.MIGRATE_HEADING('--- Simulation cycle complete. ---'))